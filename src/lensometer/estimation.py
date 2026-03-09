from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Sequence, Tuple

Point = Tuple[float, float]


@dataclass
class PrescriptionEstimate:
    sphere_diopter: float
    cylinder_diopter: float
    axis_degree: float
    confidence: float


def _solve_3x3(a: list[list[float]], b: list[float]) -> list[float]:
    # Gaussian elimination with partial pivoting.
    m = [row[:] + [val] for row, val in zip(a, b)]
    n = 3
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[pivot] = m[pivot], m[col]
        if abs(m[col][col]) < 1e-12:
            raise ValueError("Degenerate point configuration for affine fit.")
        div = m[col][col]
        for j in range(col, n + 1):
            m[col][j] /= div
        for r in range(n):
            if r == col:
                continue
            factor = m[r][col]
            for j in range(col, n + 1):
                m[r][j] -= factor * m[col][j]
    return [m[i][n] for i in range(n)]


def _fit_affine(baseline_points: Sequence[Point], lens_points: Sequence[Point]) -> list[list[float]]:
    if len(baseline_points) != len(lens_points) or len(baseline_points) < 3:
        raise ValueError("At least 3 matching points are required.")

    # Build normal equations for least squares on [x y 1] -> [u v].
    ata = [[0.0] * 3 for _ in range(3)]
    atb_u = [0.0, 0.0, 0.0]
    atb_v = [0.0, 0.0, 0.0]

    for (x, y), (u, v) in zip(baseline_points, lens_points):
        row = [x, y, 1.0]
        for i in range(3):
            for j in range(3):
                ata[i][j] += row[i] * row[j]
            atb_u[i] += row[i] * u
            atb_v[i] += row[i] * v

    sol_u = _solve_3x3(ata, atb_u)
    sol_v = _solve_3x3(ata, atb_v)

    return [
        [sol_u[0], sol_u[1], sol_u[2]],
        [sol_v[0], sol_v[1], sol_v[2]],
        [0.0, 0.0, 1.0],
    ]


def _svd_like_scales_and_axis(linear: list[list[float]]) -> tuple[float, float, float]:
    # For 2x2 matrix A, eigenvalues of A A^T -> squared singular values.
    a, b = linear[0]
    c, d = linear[1]
    m11 = a * a + b * b
    m12 = a * c + b * d
    m22 = c * c + d * d

    trace = m11 + m22
    det = m11 * m22 - m12 * m12
    disc = max(0.0, trace * trace - 4.0 * det)
    l1 = (trace + math.sqrt(disc)) / 2.0
    l2 = (trace - math.sqrt(disc)) / 2.0

    s1 = math.sqrt(max(0.0, l1))
    s2 = math.sqrt(max(0.0, l2))

    # Principal direction angle for first eigenvector of A A^T.
    if abs(m12) < 1e-12 and abs(m11 - l1) < 1e-12:
        axis = 0.0
    else:
        vx = m12
        vy = l1 - m11
        axis = math.degrees(math.atan2(vy, vx)) % 180.0
    return s1, s2, axis


def estimate_prescription(
    baseline_points: Sequence[Point],
    lens_points: Sequence[Point],
    working_distance_m: float = 0.4,
) -> PrescriptionEstimate:
    if working_distance_m <= 0:
        raise ValueError("working_distance_m must be > 0")

    affine = _fit_affine(baseline_points, lens_points)
    linear = [affine[0][:2], affine[1][:2]]
    s1, s2, axis_deg = _svd_like_scales_and_axis(linear)

    mean_scale = (s1 + s2) / 2.0
    sphere = (mean_scale - 1.0) / working_distance_m
    cylinder = abs(s1 - s2) / working_distance_m
    residual = abs(s1 - s2)
    confidence = max(0.0, min(1.0, 1.0 - residual * 3.0))

    return PrescriptionEstimate(
        sphere_diopter=round(sphere, 2),
        cylinder_diopter=round(cylinder, 2),
        axis_degree=round(axis_deg, 1),
        confidence=round(confidence, 2),
    )
