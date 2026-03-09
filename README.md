# Lensometer Mobile Prototype (High-Accuracy Focus)

Yeh repository ek **practical prototype** deta hai jo mobile camera based lens measurement workflow ka core logic implement karta hai.

## Goal

Mobile camera + calibration workflow se:
- lens power ka **approximate spherical estimate**,
- cylinder/axis ka **approximate estimate**,
- capture quality validation,
- repeatability scoring.

> Note: Yeh clinical lensometer ka replacement nahi hai. Isse screening, triage, aur pre-check ke liye design kiya gaya hai.

## Accuracy-first approach used in this prototype

1. **Reference grid calibration (must-have)**
   - Pehle baseline frame capture (without lens)
   - Phir lens frame capture (same distance/orientation)
2. **Transform-based distortion estimation**
   - Grid points par affine transform fit karke X/Y magnification nikalte hain
3. **Spherical/Cylindrical decomposition**
   - Mean magnification -> spherical estimate
   - Axis-anisotropy -> cylinder + axis estimate
4. **Quality gates**
   - blur, coverage, and geometric consistency thresholds
5. **Multi-capture averaging**
   - multiple frames leke median estimate -> better stability

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/prototype_cli.py --demo
```

## Run tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Detailed steps: `TESTING.md`

## Suggested mobile implementation stack

- Flutter/React Native camera module for capture UX
- On-device OpenCV / MediaPipe grid detection
- Is repo ka estimator module (Python logic) ko port karke mobile native module me chalaya ja sakta hai

Detailed workflow: `docs/mobile_accuracy_blueprint.md`


## Android APK prototype (aapke test ke liye)

Is repo me `android-app/` add kiya gaya hai jisme ek simple Android app hai:
- synthetic estimator run karta hai,
- output mobile screen par dikhata hai,
- APK banake phone me install kiya ja sakta hai.

Build/install steps: `APK_BUILD.md`

Quick commands:

```bash
./scripts_build_apk.sh
adb install -r android-app/app/build/outputs/apk/debug/app-debug.apk
```
