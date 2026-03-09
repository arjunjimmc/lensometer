# APK Build Guide (Android)

## 1) Prerequisites

- JDK 17+
- Android SDK (platform 34 + build-tools)
- `ANDROID_HOME` ya `ANDROID_SDK_ROOT` set hona chahiye

Example:

```bash
export ANDROID_SDK_ROOT=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin
```

## 2) Build debug APK

```bash
cd android-app
gradle assembleDebug
```

Output APK path:

```text
android-app/app/build/outputs/apk/debug/app-debug.apk
```

## 3) Install on connected Android phone

```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

## 4) Run app

- App name: **Lensometer Prototype**
- Button tap karein: **Run Synthetic Test**
- Output me sphere/cylinder/axis/quality display hoga.

> Note: Yeh abhi synthetic prototype hai (real camera pipeline next phase).
