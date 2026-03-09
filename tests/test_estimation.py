import unittest

from lensometer.estimation import estimate_prescription
from lensometer.quality import evaluate_capture_quality


class LensometerTests(unittest.TestCase):
    def test_estimate_prescription_returns_expected_signals(self) -> None:
        baseline = [(float(x), float(y)) for y in range(3) for x in range(3)]
        lens = []
        for x, y in baseline:
            lens.append((1.08 * x + 0.02 * y + 0.2, 1.03 * y - 0.1))

        result = estimate_prescription(baseline, lens, working_distance_m=0.4)

        self.assertGreater(result.sphere_diopter, 0)
        self.assertGreaterEqual(result.cylinder_diopter, 0)
        self.assertGreaterEqual(result.axis_degree, 0)
        self.assertLessEqual(result.axis_degree, 180)
        self.assertGreaterEqual(result.confidence, 0)
        self.assertLessEqual(result.confidence, 1)

    def test_quality_gate_passes_on_good_signal(self) -> None:
        pts = [(float(x), float(y)) for y in range(3) for x in range(3)]
        q = evaluate_capture_quality(
            image_laplacian_var=140,
            detected_points=pts,
            expected_points=9,
            reprojection_error_px=0.5,
        )
        self.assertTrue(q.pass_quality_gate)


if __name__ == "__main__":
    unittest.main()
