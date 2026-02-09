"""
Helper functions
"""
from pathlib import Path
from typing import List, Dict, Set

 
def save_puzzle(puzzle: dict, filepath: str) -> None:
    """
    Save puzzle to file (JSON format).
    
    Args:
        puzzle: Puzzle dictionary
        filepath: Output file path
    """
    pass


def load_puzzle(filepath: str) -> dict:
    """
    Load puzzle from file.
    
    Args:
        filepath: Path to puzzle file
    
    Returns:
        Puzzle dictionary
    """
    pass


def load_word_list(
    base_list: str = None,
    custom_lists: List[str] = None,
    min_length: int = 3,
    max_length: int = 21
) -> List[str]:
    """
    Load word list(s) and merge them.
    
    Args:
        base_list: Path to base word list (default: ENABLE)
        custom_lists: List of paths to additional word lists to merge
        min_length: Minimum word length
        max_length: Maximum word length
    
    Returns:
        Combined list of words (deduplicated, uppercase)
    
    Examples:

        # Just base list
        >>> words = load_word_list()
        
        # Add custom phrases
        >>> words = load_word_list(
        ...     custom_lists=['data/word_lists/custom_phrases.txt']
        ... )
        
        # Multiple custom lists
        >>> words = load_word_list(
        ...     custom_lists=[
        ...         'data/word_lists/custom_phrases.txt',
        ...         'data/word_lists/custom_numeric.txt'
        ...     ]
        ... )

    (see scripts folder: download_wordlist.py and create_custom_wordlist_example.py for how to use)
    """
    if base_list is None:
        base_list = Path(__file__).parent.parent / "data" / "word_lists" / "enable.txt"
    
    # Load base list
    base_list = Path(base_list)
    if not base_list.exists():
        raise FileNotFoundError(f"Base word list not found: {base_list}")
    
    with open(base_list, 'r') as f:
        words = [line.strip().upper() for line in f if line.strip()]
    
    # Load and merge custom lists
    if custom_lists:
        for custom_path in custom_lists:
            custom_path = Path(custom_path)
            if not custom_path.exists():
                print(f"Warning: Custom list not found: {custom_path}, skipping...")
                continue
            
            with open(custom_path, 'r') as f:
                custom_words = [line.strip().upper() for line in f if line.strip()]
                words.extend(custom_words)
                print(f"Added {len(custom_words):,} words from {custom_path.name}")
    
    # Filter by length
    words = [w for w in words if min_length <= len(w) <= max_length]
    
    # Remove duplicates
    words = list(set(words))
    
    print(f"Total: {len(words):,} unique words (length {min_length}-{max_length})")
    
    return words
   

def words_by_length(words: List[str]) -> Dict[int, Set[str]]:
    """
    Organize words by length for faster lookup.
    
    Args:
        words: List of words
    
    Returns:
        Dictionary mapping length -> set of words
    
    Example:
        >>> words = ['CAT', 'DOG', 'FISH', 'BIRD']
        >>> by_len = words_by_length(words)
        >>> by_len[3]
        {'CAT', 'DOG'}
        >>> by_len[4]
        {'FISH', 'BIRD'}
    """
    result = {}
    for word in words:
        length = len(word)
        if length not in result:
            result[length] = set()
        result[length].add(word)
    
    return result


def filter_words_alphanumeric(words: List[str]) -> List[str]:
    """
    Filter to only alphanumeric words (letters + digits).
    
    Args:
        words: List of words
    
    Returns:
        Filtered list containing only alphanumeric words
    """
    return [w for w in words if w.isalnum()]


def filter_words_alpha_only(words: List[str]) -> List[str]:
    """
    Filter to only alphabetic words (no digits).
    
    Args:
        words: List of words
    
    Returns:
        Filtered list containing only alphabetic words
    """
    return [w for w in words if w.isalpha()]