#!/usr/bin/env python3
"""
One-time setup script: Download the ENABLE word list
"""

import requests
from pathlib import Path

def download_enable_wordlist():
    """Download ENABLE word list to data/word_lists/enable.txt"""
    
    url = "https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt"
    output_path = Path(__file__).parent.parent / "data" / "word_lists" / "enable.txt"
    
    # Create directory if doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading ENABLE word list from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    
    # Write to file
    output_path.write_text(response.text)
    
    # Count words
    words = response.text.strip().split('\n')
    print(f"✓ Downloaded {len(words):,} words to {output_path}")
    
    return output_path

if __name__ == "__main__":
    download_enable_wordlist()