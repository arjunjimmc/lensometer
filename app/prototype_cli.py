from __future__ import annotations

import argparse

from lensometer.estimation import estimate_prescription
from lensometer.quality import evaluate_capture_quality


def build_demo_points() -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    baseline = [(float(x), float(y)) for y in range(3) for x in range(3)]
    lens_pts = []
    for x, y in baseline:
        u = 1.08 * x + 0.02 * y + 0.2
        v = 1.03 * y - 0.1
        lens_pts.append((u, v))
    return baseline, lens_pts


def main() -> None:
    parser = argparse.ArgumentParser(description="Lensometer prototype CLI")
    parser.add_argument("--demo", action="store_true", help="run synthetic demo")
    args = parser.parse_args()

    if not args.demo:
        print("Use --demo to run a synthetic prototype flow.")
        return

    baseline, lens_pts = build_demo_points()
    result = estimate_prescription(baseline, lens_pts, working_distance_m=0.4)

    quality = evaluate_capture_quality(
        image_laplacian_var=145.0,
        detected_points=lens_pts,
        expected_points=9,
        reprojection_error_px=0.6,
    )

    print("=== Lensometer Prototype Output ===")
    print(f"Sphere (D):   {result.sphere_diopter:+.2f}")
    print(f"Cylinder (D): {result.cylinder_diopter:+.2f}")
    print(f"Axis (deg):   {result.axis_degree:.1f}")
    print(f"Confidence:   {result.confidence:.2f}")
    print("--- Quality Gate ---")
    print(f"Blur score:    {quality.blur_score:.2f}")
    print(f"Coverage:      {quality.coverage_score:.2f}")
    print(f"Geometry:      {quality.geometry_score:.2f}")
    print(f"Pass quality:  {quality.pass_quality_gate}")


if __name__ == "__main__":
    main()
