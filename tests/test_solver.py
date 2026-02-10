# tests/test_solver.py

import pytest
from src.grid import CrosswordGrid
from src.solver import CrosswordSolver
from src.utils import load_word_list


def test_solver_simple_grid():
    """Test solver on a simple 5x5 grid."""
    grid = CrosswordGrid(5)
    grid.set_black_square(2, 2)  # Center black square
    
    slots = grid.extract_slots()
    overlaps = grid.calculate_overlaps(slots)
    words = load_word_list()
    
    solver = CrosswordSolver(slots, words, overlaps)
    solution = solver.solve()
    
    assert solution is not None
    assert len(solution) == len(slots)


def test_domains_initialized():
    """Test that domains are initialized correctly."""
    grid = CrosswordGrid(5)
    slots = grid.extract_slots()
    overlaps = grid.calculate_overlaps(slots)
    words = ['CAT', 'DOG', 'FISH', 'BIRD', 'TIGER']
    
    solver = CrosswordSolver(slots, words, overlaps)
    
    # All 5x5 grid slots should have length 5
    for slot in slots:
        assert slot.length == 5
        # Should only include 5-letter words
        assert 'TIGER' in solver.domains[slot]
        assert 'CAT' not in solver.domains[slot]