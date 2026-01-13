#!/usr/bin/env python3
import os
import random
import string
from pathlib import Path

# Configuration
TOTAL_FILES = 2_000_000
FILE_SIZE_KB = 10
FILE_SIZE_BYTES = FILE_SIZE_KB * 1024
FILES_PER_DIR = 1000  # Max files per directory to avoid performance issues
BASE_DIR = Path("files")


def generate_random_content(size_bytes):
    """Generate random alphanumeric content of specified size."""
    chars = string.ascii_letters + string.digits + '\n '
    return ''.join(random.choices(chars, k=size_bytes))


def create_files():
    """Create all files in nested directory structure."""
    print(
        f"Starting generation of {TOTAL_FILES:,} files ({FILE_SIZE_KB}kB each)")
    print(
        f"Total size: ~{(TOTAL_FILES * FILE_SIZE_KB) / (1024 * 1024):.2f} GB")
    print(f"Organizing into directories with max {FILES_PER_DIR} files each\n")

    # Create base directory
    BASE_DIR.mkdir(exist_ok=True)

    files_created = 0
    current_dir_index = 0
    current_file_in_dir = 0
    current_dir = None

    for i in range(TOTAL_FILES):
        # Create new directory when needed
        if current_file_in_dir == 0:
            current_dir = BASE_DIR / f"dir_{current_dir_index:06d}"
            current_dir.mkdir(exist_ok=True)

        # Create file with unique content (using file index as seed for uniqueness)
        file_path = current_dir / f"file_{current_file_in_dir:04d}.txt"
        random.seed(i)  # Unique seed per file
        content = ''.join(random.choices(
            string.ascii_letters + string.digits, k=FILE_SIZE_BYTES))
        with open(file_path, 'wb') as f:
            f.write(content.encode('utf-8'))

        files_created += 1
        current_file_in_dir += 1

        # Move to next directory if current is full
        if current_file_in_dir >= FILES_PER_DIR:
            current_file_in_dir = 0
            current_dir_index += 1

        # Progress update every 10,000 files
        if files_created % 10000 == 0:
            progress = (files_created / TOTAL_FILES) * 100
            size_gb = (files_created * FILE_SIZE_KB) / (1024 * 1024)
            print(
                f"Progress: {files_created:,}/{TOTAL_FILES:,} files ({progress:.1f}%) - {size_gb:.2f} GB")

    print(f"\n✓ Complete! Created {files_created:,} files")
    print(
        f"✓ Total size: ~{(files_created * FILE_SIZE_KB) / (1024 * 1024):.2f} GB")
    print(f"✓ Files organized in {current_dir_index + 1} directories")


if __name__ == "__main__":
    try:
        create_files()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Partial files have been created.")
    except Exception as e:
        print(f"\nError: {e}")
