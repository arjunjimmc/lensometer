from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple

Point = Tuple[float, float]


@dataclass
class CaptureQuality:
    blur_score: float
    coverage_score: float
    geometry_score: float
    pass_quality_gate: bool


def evaluate_capture_quality(
    image_laplacian_var: float,
    detected_points: Sequence[Point],
    expected_points: int,
    reprojection_error_px: float,
) -> CaptureQuality:
    coverage = 0.0 if expected_points <= 0 else min(1.0, len(detected_points) / expected_points)
    blur_score = min(1.0, image_laplacian_var / 120.0)
    geometry_score = max(0.0, min(1.0, 1.0 - reprojection_error_px / 2.5))
    passed = blur_score >= 0.45 and coverage >= 0.85 and geometry_score >= 0.6

    return CaptureQuality(
        blur_score=round(blur_score, 2),
        coverage_score=round(coverage, 2),
        geometry_score=round(geometry_score, 2),
        pass_quality_gate=passed,
    )
