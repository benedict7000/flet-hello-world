# Building APK with GitHub Actions

This project is set up to automatically build your Flet app APK using GitHub Actions.

## Setup Instructions

1. **Create a GitHub account** (if you don't have one): https://github.com/signup

2. **Create a new repository**:
   - Go to https://github.com/new
   - Name it `flet-hello-world`
   - Click "Create repository"

3. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/flet-hello-world.git
   git push -u origin main
   ```
   (Replace YOUR_USERNAME with your GitHub username)

4. **Wait for the build**:
   - Go to your repository on GitHub
   - Click "Actions" tab
   - Watch the build progress
   - When done, click the workflow run and download the APK from "Artifacts"

## What happens

- GitHub automatically builds your APK when you push code
- The build takes 20-30 minutes
- Your APK is saved as an artifact you can download
- No local Android SDK/NDK needed!

## Download your APK

1. Go to your GitHub repository
2. Click "Actions" tab
3. Click the latest workflow run
4. Scroll down to "Artifacts"
5. Download the `apk` folder
6. Extract and install on your Android device

That's it! No more local build issues.
