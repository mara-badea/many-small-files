#!/usr/bin/env python3
"""
Script to commit files directory-by-directory and push each commit.
"""

import subprocess
from pathlib import Path

BASE_DIR = Path("files")


def run_git_command(cmd):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr


def main():
    """Commit each directory and push."""
    if not BASE_DIR.exists():
        print(f"Error: {BASE_DIR} does not exist")
        return

    # Optimize git config for performance
    print("Optimizing git configuration...")
    run_git_command('git config core.preloadindex true')
    run_git_command('git config core.fscache true')
    run_git_command('git config feature.manyFiles true')
    run_git_command('git config core.untrackedCache true')

    # Get all directories
    directories = sorted([d for d in BASE_DIR.iterdir() if d.is_dir()])
    total_dirs = len(directories)

    print(f"Found {total_dirs} directories to commit")
    print(f"Each directory contains ~1,000 files (~10MB)\n")

    for i, dir_path in enumerate(directories, 1):
        dir_name = dir_path.name

        print(f"[{i}/{total_dirs}] Processing {dir_name}...")

        # Stage directory - use wildcard for faster batch add
        success, stdout, stderr = run_git_command(f'git add {dir_path}/*')
        if not success:
            print(f"  ✗ Error staging: {stdout} {stderr}")
            break

        # Commit
        commit_msg = f"Add {dir_name}"
        success, stdout, stderr = run_git_command(
            f'git commit -m "{commit_msg}"')
        if not success:
            print(f"  ✗ Error committing: {stdout} {stderr}")
            break

        # Push
        success, stdout, stderr = run_git_command('git push')
        if not success:
            print(f"  ✗ Error pushing: {stdout} {stderr}")
            break

        print(f"  ✓ Committed and pushed {dir_name}")

    print(f"\n✓ Complete! Processed {total_dirs} directories")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
