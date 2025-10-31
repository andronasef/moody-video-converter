# FFmpeg Build GitHub Action

## Overview
This workflow builds FFmpeg from source for macOS and provides a downloadable artifact.

## How to Run

1. Go to the **Actions** tab in your GitHub repository
2. Select **"Build FFmpeg for macOS"** from the workflow list
3. Click the **"Run workflow"** button
4. Select the branch you want to run it from (usually `main`)
5. Click **"Run workflow"** to start the build

## What It Does

The workflow will:
- Install all necessary build dependencies on macOS
- Download FFmpeg 6.1 source code
- Configure FFmpeg with common codec support (x264, x265, libvpx, etc.)
- Build FFmpeg using all available CPU cores
- Package the compiled binaries into a tar.gz archive
- Upload the artifact for download

## Downloading the Built FFmpeg

After the workflow completes:
1. Click on the completed workflow run
2. Scroll down to the **Artifacts** section
3. Click on the artifact name (e.g., `ffmpeg-macos-X64` or `ffmpeg-macos-ARM64`)
4. The tar.gz file will be downloaded to your computer

## Extracting and Using

```bash
# Extract the archive
tar -xzf ffmpeg-macos-*.tar.gz

# The ffmpeg, ffprobe, and ffplay binaries will be in the bin/ directory
# You can copy them to /usr/local/bin or use them directly
./bin/ffmpeg -version
```

## Build Time

The complete build process typically takes 20-30 minutes on GitHub Actions runners.

## Artifact Retention

The built FFmpeg artifact is stored for 30 days. After that, you'll need to run the workflow again to generate a new build.
