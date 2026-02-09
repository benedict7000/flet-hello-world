# Building APK for Flet App

## Prerequisites

1. Install Python 3.8 or higher
2. Install Flet: `pip install flet`

## Build APK

### Method 1: Using Flet Build Command (Recommended)

```bash
# Install flet
pip install flet

# Build APK
flet build apk
```

This will:
- Create an APK file in the `build/apk` directory
- Handle all Android SDK and build tool requirements automatically
- Use Flet's cloud build service (requires internet connection)

### Method 2: Local Build (Advanced)

For local builds, you need:
- Android SDK
- Java JDK 11+
- Gradle

```bash
# Build locally
flet build apk --local
```

## Build Options

```bash
# Build with custom app name
flet build apk --project "My Hello World App"

# Build with custom package name
flet build apk --org com.mycompany

# Build release APK (signed)
flet build apk --release

# Specify output directory
flet build apk --output-dir ./dist
```

## Testing the App

### Run on Desktop
```bash
python main.py
```

### Run on Web
```bash
flet run main.py --web
```

### Run on Mobile (Development)
```bash
# Install Flet app on your phone from Play Store/App Store
# Then run:
flet run main.py --android
# or
flet run main.py --ios
```

## APK Location

After successful build, find your APK at:
- `build/apk/app-release.apk` (release build)
- `build/apk/app-debug.apk` (debug build)

## Install APK on Android Device

1. Transfer the APK to your Android device
2. Enable "Install from Unknown Sources" in Settings
3. Open the APK file and install

## Troubleshooting

- If build fails, ensure you have internet connection (for cloud build)
- For local builds, verify Android SDK is properly installed
- Check Flet version: `flet --version`
- Update Flet: `pip install --upgrade flet`
