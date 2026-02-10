"""
Unit tests for theme.py
"""
# tests/test_theme.py

import pytest
from src.theme import ThemeManager
from src.grid import CrosswordGrid


def test_theme_word_scoring():
    """Test manual word scoring."""
    theme = ThemeManager(description="Space")
    
    theme.set_word_score("MARS", 100)
    theme.set_word_score("EARTH", 90)
    
    assert theme.get_word_score("MARS") == 100
    assert theme.get_word_score("EARTH") == 90
    assert theme.get_word_score("RANDOM") == 0  # Default


def test_theme_word_placement():
    """Test placing theme words in grid."""
    grid = CrosswordGrid(15, enforce_symmetry=True)
    grid.generate_pattern(max_slot_length=10)
    
    theme = ThemeManager(
        description="Test",
        theme_words=["TESTING", "WORDS"]
    )
    
    slots = grid.extract_slots()
    assignment = theme.place_theme_words(grid, slots)
    
    # Should place both words
    assert len(assignment) == 2
    assert "TESTING" in assignment.values()
    assert "WORDS" in assignment.values()


def test_keyword_scorer():
    """Test keyword-based scoring function."""
    def simple_scorer(word, theme):
        if "SPACE" in theme.upper() and "STAR" in word.upper():
            return 80.0
        return 0.0
    
    theme = ThemeManager(description="Space Exploration")
    words = ["STAR", "STARS", "DOG", "CAT"]
    
    theme.score_word_list(words, simple_scorer)
    
    assert theme.get_word_score("STAR") == 80.0
    assert theme.get_word_score("STARS") == 80.0
    assert theme.get_word_score("DOG") == 0.0