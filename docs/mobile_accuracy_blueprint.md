# Mobile Lensometer Accuracy Blueprint

## Best possible path for maximum accuracy (practical)

1. **Hardware jig**
   - Phone mount + fixed lens slot + fixed target distance (40 cm recommended)
   - Controlled ring light to reduce reflections
2. **Calibration card**
   - ISO printed dot-grid/checkerboard with known spacing (e.g. 5 mm)
3. **Capture protocol**
   - Baseline capture without lens
   - Lens capture with same position
   - Minimum 5 repeated captures
4. **Algorithm**
   - Sub-pixel corner/point detection
   - RANSAC-based affine/homography estimation
   - Spherical + cylindrical decomposition
   - Outlier rejection + median aggregation
5. **Validation loop**
   - Compare against clinical lensometer labels
   - Train correction regressor for device model-specific bias

## Mobile app UX flow

1. Start scan
2. Auto alignment guide (distance + tilt)
3. Baseline capture
4. Insert lens and capture burst
5. Quality gate + retake if needed
6. Output (Sphere/Cyl/Axis + confidence + warning)

## Safety

- App output should include: "For screening use only. Clinical confirmation required."
