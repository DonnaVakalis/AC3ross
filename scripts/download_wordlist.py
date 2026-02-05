#!/usr/bin/env python3
"""
Setup script: Download word lists
"""

import os
import sys
import urllib.request
from pathlib import Path


def download_enable_wordlist(output_path: str) -> None:
    """
    Download the ENABLE word list.
    
    Args:
        output_path: Path where word list will be saved
    """
    enable_url = "https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt"
    
    print(f"Downloading ENABLE word list to {output_path}...")
    try:
        urllib.request.urlretrieve(enable_url, output_path)
        print(f"Successfully downloaded word list to {output_path}")
    except Exception as e:
        print(f"Error downloading word list: {e}")
        sys.exit(1)


def main():
    """Main function"""
    # Get the project root directory (parent of scripts/)
    project_root = Path(__file__).parent.parent
    word_list_dir = project_root / "data" / "word_lists"
    word_list_dir.mkdir(parents=True, exist_ok=True)
    
    enable_path = word_list_dir / "enable.txt"
    
    if enable_path.exists():
        response = input(f"{enable_path} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Skipping download.")
            return
    
    download_enable_wordlist(str(enable_path))


if __name__ == "__main__":
    main()

