"""
Example: Creating custom word lists for crossword puzzles.

This script demonstrates how to:
1. Create custom phrase lists (multi-word answers)
2. Create numeric/alphanumeric lists
3. Create theme-specific lists
4. Load and merge them with the base ENABLE list
"""
import sys
from pathlib import Path

# Add project root to Python path so we can import src
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils import load_word_list

def create_example_custom_lists():
    """Create example custom word lists."""
    
    word_lists_dir = Path(__file__).parent.parent / "data" / "word_lists"
    word_lists_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Multi-word phrases (concatenated without spaces)
    phrases = [
        "IMONIT",       # "I'm on it"
        "LETITGO",      # "Let it go"
        "ONTHERUN",     # "On the run"
        "GOODTOGO",     # "Good to go"
        "ALLSET",       # "All set"
        "NOTEVENCLOSE", # "Not even close"
    ]
    
    phrases_path = word_lists_dir / "user_custom_phrases.txt"
    phrases_path.write_text('\n'.join(phrases))
    print(f"✓ Created {phrases_path} with {len(phrases)} phrases")
    
    # 2. Numeric/alphanumeric entries
    numeric = [
        "314",          # Pi without decimal
        "CO2",          # Carbon dioxide
        "H2O",          # Water
        "ROUTE66",      # Famous highway
        "AREA51",       # Famous location
        "MP3",          # Audio format
        "TYPE2",        # As in "Type 2 diabetes"
    ]
    
    numeric_path = word_lists_dir / "user_custom_numeric.txt"
    numeric_path.write_text('\n'.join(numeric))
    print(f"✓ Created {numeric_path} with {len(numeric)} entries")
    
    # 3. Theme-specific: AI/ML (example)
    ai_terms = [
        "NEURALNET",
        "DEEPLEARNING",
        "MACHINELEARNING",
        "REINFORCEMENTLEARNING",
        "GRADIENTDESCENT",
        "BACKPROP",
        "TRANSFORMER",
        "LLMS",
    ]
    
    ai_path = word_lists_dir / "user_custom_theme_ai.txt"
    ai_path.write_text('\n'.join(ai_terms))
    print(f"✓ Created {ai_path} with {len(ai_terms)} AI terms")
    
    print("\n" + "="*60)
    print("Example custom word lists created!")
    print("="*60)


def demo_loading_custom_lists():
    """Demonstrate loading and merging word lists."""
    
    print("\n--- Loading base ENABLE list only ---")
    base_words = load_word_list()
    print(f"Base list has: {len(base_words):,} words")
    print(f"Contains 'IMONIT'? {('IMONIT' in base_words)}")  # False
    
    print("\n--- Loading with custom phrases ---")
    words_with_phrases = load_word_list(
        custom_lists=['data/word_lists/user_custom_phrases.txt']
    )
    print(f"Combined list has: {len(words_with_phrases):,} words")
    print(f"Contains 'IMONIT'? {('IMONIT' in words_with_phrases)}")  # True
    
    print("\n--- Loading with ALL custom lists ---")
    all_words = load_word_list(
        custom_lists=[
            'data/word_lists/user_custom_phrases.txt',
            'data/word_lists/user_custom_numeric.txt',
            'data/word_lists/user_custom_theme_ai.txt',
        ]
    )
    print(f"Full combined list has: {len(all_words):,} words")
    print(f"Contains 'IMONIT'? {('IMONIT' in all_words)}")
    print(f"Contains 'CO2'? {('CO2' in all_words)}")
    print(f"Contains 'NEURALNET'? {('NEURALNET' in all_words)}")


if __name__ == "__main__":
    # Create example lists
    create_example_custom_lists()
    
    # Show how to load them
    demo_loading_custom_lists()