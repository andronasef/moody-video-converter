# Moody Video Converter

A user-friendly video converter application that resizes videos to vertical (1080x1920) format with letterboxing, perfect for social media platforms like Instagram Stories, TikTok, and YouTube Shorts.

## Features

- 🎥 Convert videos to vertical format (1080x1920)
- 🖼️ Automatic letterboxing with black padding
- 📁 Batch processing support
- 🎨 Modern dark-themed UI
- ⚡ Multi-threaded processing for responsive interface

## Building the Application

### Build for macOS (Using GitHub Actions)

The easiest way to build the macOS application is using the provided GitHub Action:

1. **Navigate to Actions Tab**
   - Go to your GitHub repository
   - Click on the "Actions" tab at the top

2. **Run the Workflow**
   - Select "Build macOS App with FFmpeg" from the workflows list
   - Click the "Run workflow" button (green button on the right)
   - Select the branch (usually `main` or your current branch)
   - Click "Run workflow" to start the build

3. **Download the Build**
   - Wait for the workflow to complete (usually 5-10 minutes)
   - Once completed, scroll down to the "Artifacts" section
   - Click on "VideoConverter-macOS" to download the ZIP file
   - The artifact is available for 30 days

4. **Install and Run**
   - Extract the ZIP file
   - Double-click `VideoConverter.app` to run
   - If macOS shows a security warning, go to System Preferences > Security & Privacy and allow the app

### Manual Build (Local Development)

If you prefer to build locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Install FFmpeg (macOS)
brew install ffmpeg

# Run the application
python converter_app.py

# Or build with PyInstaller
pyinstaller --name="VideoConverter" \
  --windowed \
  --onedir \
  --add-binary="$(which ffmpeg):." \
  converter_app.py
```

## Requirements

### Python Dependencies
- customtkinter >= 5.2.0
- ffmpeg-python >= 0.2.0
- pyinstaller >= 6.0.0 (for building)

### System Requirements
- FFmpeg (included in the built application)
- Python 3.8+ (for development)

## Usage

1. Launch the application
2. Click "Select Videos" to choose one or more video files
3. Selected videos appear in the queue
4. Click "Start Conversion" to begin processing
5. Converted videos are saved in the same directory as the original files with "Resized" suffix

## Supported Formats

- MP4
- MOV
- AVI
- MKV

## Technical Details

- Output resolution: 1080x1920 (vertical)
- Maintains aspect ratio with letterboxing
- Video codec: H.264 (libx264)
- Audio: copied without re-encoding

## License

This project is open source and available for use and modification.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
