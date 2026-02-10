# scripts/test_custom_wordlist_scoring.py
"""
Test how strongly word scoring influences puzzle generation.
 
"""

import sys
from pathlib import Path

# Add project root to Python path so we can import src
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.grid import CrosswordGrid
from src.solver import CrosswordSolver
from src.theme import ThemeManager
from src.utils import load_word_list


GRID_SIZE = 12
MAX_SLOT_LENGTH = 6
BLCK_PRCTG = 0.2
influence_value = 10.0


def main():
    print("="*50)
    print("Custom Word List Scoring Test with influence value set to: {influence_value}")
    print("="*50)
    
    # 1. Load main word list
    print("\n1. Loading word lists...")
    main_words = load_word_list('data/word_lists_raw/enable.txt')
    print(f"   Main list: {len(main_words):,} words")
    
    # 2. Load custom AI/ML word list
    custom_path = Path('data/word_lists_raw/ai_ml.txt')
    if not custom_path.exists():
        print(f"\nError: {custom_path} not found!")
        print("Create this file with your AI/ML words (one per line)")
        return
    
    with open(custom_path, 'r') as f:
        custom_words = [line.strip().upper() for line in f if line.strip()]
    
    print(f"   Custom AI/ML list: {len(custom_words)} words")
    
    # 3. Create theme and score words
    print("\n2. Scoring words...")
    theme = ThemeManager(description="AI/ML Custom Words")
    for word in custom_words:
        theme.set_word_score(word, 100.0)
    
    # All other words get default score of 0 (no need to explicitly set)
    
    print(f"...{len(custom_words)} words scored at 100")
    print(f"...{len(main_words) - len(custom_words):,} words scored at 0 (default)")
    
    # 4. Create grid
    print("\n3. Creating grid...")
    grid = CrosswordGrid(GRID_SIZE, enforce_symmetry=True)
    grid.generate_pattern(black_percentage=BLCK_PRCTG,max_slot_length=MAX_SLOT_LENGTH)
    
    print(grid)
    grid.print_grid_info()
    
    # 5. Extract slots
    slots = grid.extract_slots()
    overlaps = grid.calculate_overlaps(slots)
    
    # 6. Combine word lists
    all_words = list(set(main_words + custom_words))
    print(f"\n4. Total vocabulary: {len(all_words):,} words")
    
    # 7. Solver is up next! (now with more influence flexibility :) 
    print("\n5. Solving puzzle...")
    solver = CrosswordSolver(slots, all_words, overlaps, theme=theme, theme_influence=influence_value)
    solution = solver.solve()
    
    # 8. Analyze results
    if solution:
        print("\n" + "="*60)
        print("SOLUTION FOUND!")
        print("="*60)
        
        # Fill grid
        for slot, word in solution.items():
            for i, (row, col) in enumerate(slot.cells):
                grid.set_cell(row, col, word[i])
        
        print()
        grid.visualize_filled()
        
        # Analyze word usage
        print("\n" + "="*60)
        print("WORD USAGE ANALYSIS")
        print("="*60)
        
        high_scored_words = []
        zero_scored_words = []
        
        for slot, word in solution.items():
            score = theme.get_word_score(word)
            if score == 100:
                high_scored_words.append(word)
            else:
                zero_scored_words.append(word)
        
        total_words = len(solution)
        high_count = len(high_scored_words)
        zero_count = len(zero_scored_words)
        
        print(f"\nTotal words in puzzle: {total_words}")
        print(f"High-scored words (100): {high_count} ({high_count/total_words*100:.1f}%)")
        print(f"Zero-scored words (0):   {zero_count} ({zero_count/total_words*100:.1f}%)")
        
        if high_scored_words:
            print(f"\nHigh-scored words used:")
            for word in sorted(high_scored_words):
                print(f"  ★ {word}")
        
        if zero_scored_words:
            print(f"\nZero-scored words used:")
            for word in sorted(zero_scored_words):
                print(f"  · {word}")
        
        # Calculate influence
        print("\n" + "="*60)
        print("SCORING INFLUENCE")
        print("="*60)
        
        custom_words_set = set(w.upper() for w in custom_words)
        available_custom = len([w for w in all_words if w in custom_words_set])
        available_percent = available_custom / len(all_words) * 100
        used_percent = high_count / total_words * 100
        
        print(f"Custom words in vocabulary: {available_custom} ({available_percent:.2f}%)")
        print(f"Custom words in solution:   {high_count} ({used_percent:.1f}%)")
        
        if used_percent > available_percent:
            boost = used_percent / available_percent
            print(f"\n✓ Scoring boosted usage by {boost:.1f}x!")
        else:
            print(f"\n⚠ Scoring had minimal effect")
        
    else:
        print("\n✗ No solution found")
        print("Try:")
        print("  - Regenerating the grid")
        print("  - Using a larger grid")
        print("  - Adding more words to ai_ml.txt")


if __name__ == "__main__":
    main()