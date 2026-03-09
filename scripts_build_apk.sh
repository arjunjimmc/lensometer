#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${ANDROID_SDK_ROOT:-}" && -z "${ANDROID_HOME:-}" ]]; then
  echo "ERROR: ANDROID_SDK_ROOT or ANDROID_HOME set nahi hai."
  exit 1
fi

cd android-app
gradle assembleDebug

echo "APK ready: app/build/outputs/apk/debug/app-debug.apk"
