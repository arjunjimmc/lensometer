package com.lensometer.prototype

import org.junit.Assert.assertTrue
import org.junit.Test

class EstimatorTest {
    @Test
    fun estimate_has_valid_ranges() {
        val baseline = buildList {
            for (y in 0..2) for (x in 0..2) add(Point(x.toDouble(), y.toDouble()))
        }
        val lens = baseline.map { p -> Point(1.08 * p.x + 0.02 * p.y + 0.2, 1.03 * p.y - 0.1) }
        val r = Estimator.estimatePrescription(baseline, lens)
        assertTrue(r.sphereDiopter > 0)
        assertTrue(r.axisDegree in 0.0..180.0)
        assertTrue(r.confidence in 0.0..1.0)
    }
}
