#!/usr/bin/env python3
"""
Command line tool to generate crossword puzzles
Example:
python scripts/generate.py --width 15 --height 15 --theme PYTHON CODING AI --output output/puzzle.json
"""

import argparse
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from grid import create_grid
from solver import solve_crossword
from theme import place_theme_words
from clues import generate_all_clues
from utils import load_word_list, save_puzzle


def generate_crossword(width: int, height: int, word_list_path: str, 
                       theme_words: list = None, output_path: str = None) -> dict:
    """
    Generate a crossword puzzle.
    
    Args:
        width: Grid width
        height: Grid height
        word_list_path: Path to word list file
        theme_words: Optional list of theme words
        output_path: Optional output file path
    
    Returns:
        Generated puzzle dictionary
    """
    # Load word list
    word_list = load_word_list(word_list_path)
    
    # Create grid
    grid = create_grid(width, height)
    
    # Place theme words if provided
    if theme_words:
        theme_placement = place_theme_words(grid, theme_words)
    else:
        theme_placement = {}
    
    # Solve crossword
    solution = solve_crossword(grid, word_list)
    
    # Generate clues
    clues = generate_all_clues(solution)
    
    # Assemble puzzle
    puzzle = {
        "grid": grid,
        "solution": solution,
        "clues": clues,
        "theme_words": theme_placement
    }
    
    # Save if output path provided
    if output_path:
        save_puzzle(puzzle, output_path)
        print(f"Puzzle saved to {output_path}")
    
    return puzzle


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Generate crossword puzzles")
    parser.add_argument("--width", type=int, default=15, help="Grid width (default: 15)")
    parser.add_argument("--height", type=int, default=15, help="Grid height (default: 15)")
    parser.add_argument("--word-list", type=str, 
                       default="data/word_lists/enable.txt",
                       help="Path to word list file")
    parser.add_argument("--theme", nargs="+", help="Theme words to include")
    parser.add_argument("--output", type=str, help="Output file path")
    
    args = parser.parse_args()
    
    # Resolve paths relative to project root
    project_root = Path(__file__).parent.parent
    word_list_path = project_root / args.word_list
    
    if not word_list_path.exists():
        print(f"Error: Word list not found at {word_list_path}")
        print("Run scripts/download_wordlist.py first to download the word list.")
        sys.exit(1)
    
    output_path = None
    if args.output:
        output_path = project_root / args.output
    
    puzzle = generate_crossword(
        args.width,
        args.height,
        str(word_list_path),
        args.theme,
        str(output_path) if output_path else None
    )
    
    print("Crossword puzzle generated successfully!")


if __name__ == "__main__":
    main()

