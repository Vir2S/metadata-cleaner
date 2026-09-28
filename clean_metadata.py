#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".heic",
    ".tiff",
    ".mp3",
    ".m4a",
    ".wav",
    ".flac",
    ".mp4",
    ".mov",
    ".mkv",
    ".pdf",
}

MUSIC_EXTENSIONS = {".mp3", ".m4a", ".flac", ".wav"}

MUSIC_TAGS_TO_KEEP = (
    "Title",
    "Artist",
    "Album",
    "AlbumArtist",
    "Track",
    "DiscNumber",
    "Genre",
    "Year",
    "Date",
    "CoverArt",
    "Picture",
    "Artwork",
)


def check_exiftool() -> None:
    if shutil.which("exiftool") is None:
        print("Error: exiftool is not installed.")
        print("macOS: brew install exiftool")
        print("Ubuntu/Debian: sudo apt install libimage-exiftool-perl")
        sys.exit(1)


def build_command(file_path: Path, keep_music_tags: bool) -> list[str]:
    command = ["exiftool", "-all=", "-overwrite_original"]

    if keep_music_tags and file_path.suffix.lower() in MUSIC_EXTENSIONS:
        for tag in MUSIC_TAGS_TO_KEEP:
            command.append(f"-tagsFromFile")
            command.append("@")
            command.append(f"-{tag}")

    command.append(str(file_path))
    return command


def clean_metadata(file_path: Path, dry_run: bool, keep_music_tags: bool) -> bool:
    prefix = "[DRY RUN] " if dry_run else ""
    print(f"{prefix}Cleaning: {file_path}")

    if dry_run:
        return True

    result = subprocess.run(
        build_command(file_path, keep_music_tags),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        print(f"Failed: {file_path}")
        if result.stderr.strip():
            print(result.stderr.strip())
        return False

    return True


def iter_files(target: Path, recursive: bool):
    if target.is_file():
        if target.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield target
        return

    pattern = "**/*" if recursive else "*"
    for path in target.glob(pattern):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def process_path(target: Path, recursive: bool, dry_run: bool, keep_music_tags: bool) -> None:
    if not target.exists():
        print(f"Path does not exist: {target}")
        sys.exit(1)

    files = list(iter_files(target, recursive))
    if not files:
        print("No supported files found.")
        return

    cleaned = 0
    failed = 0

    for file_path in files:
        if clean_metadata(file_path, dry_run, keep_music_tags):
            cleaned += 1
        else:
            failed += 1

    print()
    print(f"Processed: {cleaned + failed}")
    print(f"Cleaned:   {cleaned}")
    print(f"Failed:    {failed}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove metadata from files using ExifTool."
    )
    parser.add_argument("path", type=Path, help="File or directory to process")
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Process directories recursively",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show files without modifying them",
    )
    parser.add_argument(
        "--keep-music-tags",
        action="store_true",
        help="Preserve common music tags for audio files while removing other metadata",
    )

    args = parser.parse_args()
    check_exiftool()
    process_path(
        target=args.path.expanduser().resolve(),
        recursive=args.recursive,
        dry_run=args.dry_run,
        keep_music_tags=args.keep_music_tags,
    )


if __name__ == "__main__":
    main()
