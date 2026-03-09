package com.lensometer.prototype

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val runBtn = findViewById<Button>(R.id.runDemoBtn)
        val output = findViewById<TextView>(R.id.output)

        runBtn.setOnClickListener {
            val baseline = buildList {
                for (y in 0..2) for (x in 0..2) add(Point(x.toDouble(), y.toDouble()))
            }
            val lens = baseline.map { p ->
                Point(
                    x = 1.08 * p.x + 0.02 * p.y + 0.2,
                    y = 1.03 * p.y - 0.1
                )
            }

            val estimate = Estimator.estimatePrescription(baseline, lens, 0.4)
            val quality = Estimator.evaluateCaptureQuality(145.0, lens.size, 9, 0.6)

            output.text = """
                Sphere (D):   ${"%+.2f".format(estimate.sphereDiopter)}
                Cylinder (D): ${"%+.2f".format(estimate.cylinderDiopter)}
                Axis (deg):   ${"%.1f".format(estimate.axisDegree)}
                Confidence:   ${"%.2f".format(estimate.confidence)}

                Blur score:   ${"%.2f".format(quality.blurScore)}
                Coverage:     ${"%.2f".format(quality.coverageScore)}
                Geometry:     ${"%.2f".format(quality.geometryScore)}
                Pass quality: ${quality.passQualityGate}

                Note: Screening-only prototype.
            """.trimIndent()
        }
    }
}
