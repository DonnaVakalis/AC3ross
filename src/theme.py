"""
Theme word placement & scoring
"""

import sys
from pathlib import Path

# Add project root to Python path so we can import src
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    
from typing import List, Dict, Set, Optional
from src.grid import CrosswordGrid, Slot


class ThemeManager:
    """
    Manages theme words and theme-based word scoring.
    
    Supports:
    - Hard constraints: Specific words that MUST appear
    - Soft constraints: Scoring system to prefer theme-related words
    """
    
    def __init__(self, description: str = None, theme_words: List[str] = None):
        """
        Initialize theme manager.
        
        Args:
            description: Text description of the theme (e.g., "Artificial Intelligence")
            theme_words: List of required theme words (uppercase)
        
        Example:
            >>> theme = ThemeManager(
            ...     description="Space Exploration",
            ...     theme_words=["MARS", "ASTRONAUT", "ROCKET"]
            ... )
        """
        self.description = description
        self.theme_words = [w.upper() for w in (theme_words or [])]
        
        # Word scores: maps word -> score (0-100)
        # 0 = neutral/unrelated, 100 = highly related
        self.word_scores = {}
    
    def set_word_score(self, word: str, score: float):
        """
        Set theme relevance score for a word.
        
        Args:
            word: Word to score (will be uppercased)
            score: Relevance score (0-100)
                   0 = unrelated to theme
                   100 = highly related to theme
        """
        word = word.upper()
        if not (0 <= score <= 100):
            raise ValueError(f"Score must be 0-100, got {score}")
        self.word_scores[word] = score
    
    def get_word_score(self, word: str) -> float:
        """
        Get theme relevance score for a word.
        
        Args:
            word: Word to score
        
        Returns:
            Score (0-100), or 0 if not scored
        """
        return self.word_scores.get(word.upper(), 0.0)
    
    def score_word_list(self, words: List[str], scorer_func) -> Dict[str, float]:
        """
        Score a list of words using a custom scoring function.
        
        Args:
            words: List of words to score
            scorer_func: Function that takes (word, theme_description) -> score (0-100)
        
        Returns:
            Dictionary mapping words to scores
        
        Example:
            >>> def simple_scorer(word, theme):
            ...     # Simple keyword matching
            ...     if 'SPACE' in theme.upper():
            ...         if 'STAR' in word or 'MOON' in word:
            ...             return 80.0
            ...     return 0.0
            >>> 
            >>> theme.score_word_list(words, simple_scorer)
        """
        if self.description is None:
            raise ValueError("Theme description required for scoring")
        
        for word in words:
            score = scorer_func(word, self.description)
            self.set_word_score(word, score)
        
        return self.word_scores
    
    def place_theme_words(self, grid: CrosswordGrid, slots: List[Slot]) -> Dict[Slot, str]:
        """
        Find placement for required theme words in the grid.
        
        Args:
            grid: CrosswordGrid instance
            slots: List of available slots
        
        Returns:
            Dictionary mapping slots to theme words (partial assignment)
        
        Strategy:
            - Match theme words to slots by length
            - Prefer longer theme words first (harder to place)
            - Return assignment of theme words to slots
        
        Raises:
            ValueError: If theme words cannot be placed (no matching slots)
        """
        assignment = {}
        
        # Sort theme words by length (longest first - harder to place)
        sorted_theme_words = sorted(self.theme_words, key=len, reverse=True)
        
        # Track which slots are used
        used_slots = set()
        
        for theme_word in sorted_theme_words:
            # Find slots that match this word's length
            matching_slots = [s for s in slots 
                            if s.length == len(theme_word) 
                            and s not in used_slots]
            
            if not matching_slots:
                raise ValueError(
                    f"Cannot place theme word '{theme_word}' (length {len(theme_word)}). "
                    f"No available slots of that length."
                )
            
            # For now, pick first matching slot
            # TODO: Could use heuristics (prefer central positions, etc.)
            slot = matching_slots[0]
            assignment[slot] = theme_word
            used_slots.add(slot)
        
        return assignment
    
    def get_theme_info(self) -> Dict:
        """
        Export theme information for metadata/clue generation.
        
        Returns:
            Dictionary with theme details
        """
        return {
            'description': self.description,
            'theme_words': self.theme_words,
            'scored_words_count': len(self.word_scores),
            'high_scoring_words': sorted(
                [(w, s) for w, s in self.word_scores.items() if s >= 70],
                key=lambda x: x[1],
                reverse=True
            )[:20]  # Top 20 high-scoring words
        }