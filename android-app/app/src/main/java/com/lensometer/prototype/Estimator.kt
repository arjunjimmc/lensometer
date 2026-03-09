package com.lensometer.prototype

import kotlin.math.abs
import kotlin.math.atan2
import kotlin.math.max
import kotlin.math.min
import kotlin.math.sqrt

data class PrescriptionEstimate(
    val sphereDiopter: Double,
    val cylinderDiopter: Double,
    val axisDegree: Double,
    val confidence: Double
)

data class CaptureQuality(
    val blurScore: Double,
    val coverageScore: Double,
    val geometryScore: Double,
    val passQualityGate: Boolean
)

data class Point(val x: Double, val y: Double)

object Estimator {
    fun estimatePrescription(
        baseline: List<Point>,
        lens: List<Point>,
        workingDistanceM: Double = 0.4
    ): PrescriptionEstimate {
        require(workingDistanceM > 0) { "workingDistanceM must be > 0" }
        val affine = fitAffine(baseline, lens)
        val linear = arrayOf(
            doubleArrayOf(affine[0][0], affine[0][1]),
            doubleArrayOf(affine[1][0], affine[1][1])
        )
        val (s1, s2, axisDeg) = scalesAndAxis(linear)
        val meanScale = (s1 + s2) / 2.0
        val sphere = (meanScale - 1.0) / workingDistanceM
        val cylinder = abs(s1 - s2) / workingDistanceM
        val confidence = max(0.0, min(1.0, 1.0 - abs(s1 - s2) * 3.0))
        return PrescriptionEstimate(
            sphereDiopter = round2(sphere),
            cylinderDiopter = round2(cylinder),
            axisDegree = round1(axisDeg),
            confidence = round2(confidence)
        )
    }

    fun evaluateCaptureQuality(
        imageLaplacianVar: Double,
        detectedPoints: Int,
        expectedPoints: Int,
        reprojectionErrorPx: Double
    ): CaptureQuality {
        val coverage = if (expectedPoints <= 0) 0.0 else min(1.0, detectedPoints.toDouble() / expectedPoints)
        val blur = min(1.0, imageLaplacianVar / 120.0)
        val geometry = max(0.0, min(1.0, 1.0 - reprojectionErrorPx / 2.5))
        val pass = blur >= 0.45 && coverage >= 0.85 && geometry >= 0.6
        return CaptureQuality(round2(blur), round2(coverage), round2(geometry), pass)
    }

    private fun fitAffine(baseline: List<Point>, lens: List<Point>): Array<DoubleArray> {
        require(baseline.size == lens.size && baseline.size >= 3) { "Need at least 3 matching points" }
        val ata = Array(3) { DoubleArray(3) }
        val atbU = DoubleArray(3)
        val atbV = DoubleArray(3)
        for (i in baseline.indices) {
            val x = baseline[i].x
            val y = baseline[i].y
            val u = lens[i].x
            val v = lens[i].y
            val row = doubleArrayOf(x, y, 1.0)
            for (r in 0..2) {
                for (c in 0..2) ata[r][c] += row[r] * row[c]
                atbU[r] += row[r] * u
                atbV[r] += row[r] * v
            }
        }
        val su = solve3x3(ata, atbU)
        val sv = solve3x3(ata, atbV)
        return arrayOf(
            doubleArrayOf(su[0], su[1], su[2]),
            doubleArrayOf(sv[0], sv[1], sv[2]),
            doubleArrayOf(0.0, 0.0, 1.0)
        )
    }

    private fun solve3x3(a: Array<DoubleArray>, b: DoubleArray): DoubleArray {
        val m = Array(3) { r -> DoubleArray(4).also { c ->
            for (j in 0..2) c[j] = a[r][j]
            c[3] = b[r]
        }}
        for (col in 0..2) {
            var pivot = col
            for (r in (col + 1)..2) if (abs(m[r][col]) > abs(m[pivot][col])) pivot = r
            val tmp = m[col]; m[col] = m[pivot]; m[pivot] = tmp
            require(abs(m[col][col]) > 1e-12) { "Degenerate config" }
            val div = m[col][col]
            for (j in col..3) m[col][j] /= div
            for (r in 0..2) {
                if (r == col) continue
                val factor = m[r][col]
                for (j in col..3) m[r][j] -= factor * m[col][j]
            }
        }
        return doubleArrayOf(m[0][3], m[1][3], m[2][3])
    }

    private fun scalesAndAxis(linear: Array<DoubleArray>): Triple<Double, Double, Double> {
        val a = linear[0][0]; val b = linear[0][1]
        val c = linear[1][0]; val d = linear[1][1]
        val m11 = a * a + b * b
        val m12 = a * c + b * d
        val m22 = c * c + d * d
        val trace = m11 + m22
        val det = m11 * m22 - m12 * m12
        val disc = max(0.0, trace * trace - 4.0 * det)
        val l1 = (trace + sqrt(disc)) / 2.0
        val l2 = (trace - sqrt(disc)) / 2.0
        val s1 = sqrt(max(0.0, l1))
        val s2 = sqrt(max(0.0, l2))
        val axis = if (abs(m12) < 1e-12 && abs(m11 - l1) < 1e-12) 0.0
        else (Math.toDegrees(atan2(l1 - m11, m12)) + 180.0) % 180.0
        return Triple(s1, s2, axis)
    }

    private fun round2(v: Double): Double = kotlin.math.round(v * 100.0) / 100.0
    private fun round1(v: Double): Double = kotlin.math.round(v * 10.0) / 10.0
}
