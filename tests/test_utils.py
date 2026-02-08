"""Tests for utility functions and word list loading."""

import pytest
from src.utils import load_word_list, words_by_length, filter_words_alpha_only


def test_load_word_list():
    """Test loading word list."""
    words = load_word_list()
    
    # Should have loaded many words
    assert len(words) > 100000
    
    # Words should be uppercase
    assert all(w.isupper() for w in words[:100])
    
    # Should contain common words
    assert 'CAT' in words
    assert 'DOG' in words


def test_load_word_list_min_length():
    """Test filtering by minimum length."""
    words = load_word_list(min_length=5)
    
    # All words should be >= 5 letters
    assert all(len(w) >= 5 for w in words)


def test_load_word_list_max_length():
    """Test filtering by maximum length."""
    words = load_word_list(max_length=10)
    
    # All words should be <= 10 letters
    assert all(len(w) <= 10 for w in words)


def test_words_by_length():
    """Test organizing words by length."""
    words = ['CAT', 'DOG', 'FISH', 'BIRD', 'ELEPHANT']
    by_len = words_by_length(words)
    
    assert len(by_len[3]) == 2  # CAT, DOG
    assert len(by_len[4]) == 2  # FISH, BIRD
    assert len(by_len[8]) == 1  # ELEPHANT
    
    assert 'CAT' in by_len[3]
    assert 'FISH' in by_len[4]


def test_filter_alpha_only():
    """Test filtering to alphabetic words only."""
    words = ['CAT', 'DOG', '314', 'PI2', 'FISH']
    alpha = filter_words_alpha_only(words)
    
    assert alpha == ['CAT', 'DOG', 'FISH']