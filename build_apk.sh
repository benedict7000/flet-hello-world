#!/bin/bash
set -e

echo "Activating virtual environment..."
source venv/bin/activate

echo "Building APK with Buildozer..."
buildozer android debug

echo ""
echo "Build complete!"
echo "APK location: bin/helloworld-1.0.0-arm64-v8a_armeabi-v7a-debug.apk"
