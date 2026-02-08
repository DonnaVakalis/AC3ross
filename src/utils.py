"""
Helper functions
"""
from pathlib import Path
from typing import List, Dict, Set

def load_word_list(filepath: str) -> list:
    """
    Load word list from file.
    
    Args:
        filepath: Path to word list file
    
    Returns:
        List of words
    """
    pass


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


def load_word_list(filepath: str = None, min_length: int = 3, max_length: int = 21) -> List[str]:
    """
    Load word list from file.
    
    Args:
        filepath: Path to word list file. If None, uses default ENABLE list.
        min_length: Minimum word length to include (default 3)
        max_length: Maximum word length to include (default 21)
    
    Returns:
        List of words (uppercase, filtered by length)
    
    Example:
        >>> words = load_word_list()
        >>> len(words)
        172820
        >>> words[0]
        'AA'
    """
    if filepath is None:
        # Default to ENABLE word list
        filepath = Path(__file__).parent.parent / "data" / "word_lists" / "enable.txt"
    
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(
            f"Word list not found at {filepath}. "
            f"Run 'python scripts/download_wordlist.py' to download it."
        )
    
    # Load and process words
    with open(filepath, 'r') as f:
        words = [line.strip().upper() for line in f if line.strip()]
    
    # Filter by length
    words = [w for w in words if min_length <= len(w) <= max_length]
    
    # Remove duplicates (shouldn't be any, but just in case)
    words = list(set(words))
    
    print(f"Loaded {len(words):,} words (length {min_length}-{max_length})")
    
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