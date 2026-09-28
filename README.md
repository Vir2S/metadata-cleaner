# Metadata Cleaner

Small Python CLI utility for removing metadata from images, audio, video, and PDF files using ExifTool.

## Features

- Clean a single file or an entire directory.
- Recursive directory processing.
- Dry-run mode.
- No `_original` backup files created by ExifTool.
- Optional music-safe mode that preserves common music tags.
- Supports JPG, JPEG, PNG, WEBP, HEIC, TIFF, MP3, M4A, WAV, FLAC, MP4, MOV, MKV, and PDF.

## Requirements

- Python 3.9+
- ExifTool

### macOS

```bash
brew install exiftool
```

### Ubuntu / Debian

```bash
sudo apt install libimage-exiftool-perl
```

## Usage

Clean one file:

```bash
python3 clean_metadata.py photo.jpg
```

Clean all supported files in a directory:

```bash
python3 clean_metadata.py ~/Downloads
```

Clean recursively:

```bash
python3 clean_metadata.py ~/Downloads --recursive
```

Preview files without changing them:

```bash
python3 clean_metadata.py ~/Downloads --recursive --dry-run
```

For music releases, preserve common tags such as title, artist, album, year, track number, and artwork:

```bash
python3 clean_metadata.py song.m4a --keep-music-tags
```

You can combine options:

```bash
python3 clean_metadata.py ~/Music --recursive --keep-music-tags
```

## Important

Metadata is removed in place. Keep a backup of important files before bulk processing.
