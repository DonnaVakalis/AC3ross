"""
Unit tests for grid.py
Contains the CrosswordGrid class for managing puzzle structure.
"""

import pytest
from src.grid import CrosswordGrid


# Basic creation tests
def test_create_square_grid():
    """Test creating a square grid."""
    grid = CrosswordGrid(15)
    assert grid.width == 15
    assert grid.height == 15
    assert len(grid.grid) == 15
    assert len(grid.grid[0]) == 15


def test_create_rectangular_grid():
    """Test creating a rectangular grid."""
    grid = CrosswordGrid(15, 21)
    assert grid.width == 15
    assert grid.height == 21


def test_grid_initially_empty():
    """Test that new grid has all None cells."""
    grid = CrosswordGrid(5)
    for row in grid.grid:
        for cell in row:
            assert cell is None


# Black square tests
def test_set_black_square():
    """Test setting a black square."""
    grid = CrosswordGrid(5)
    grid.set_black_square(0, 0)
    assert grid.is_black(0, 0)
    assert grid.get_cell(0, 0) == '#'


def test_set_cell_with_hash():
    """Test that set_cell with '#' creates black square."""
    grid = CrosswordGrid(5)
    grid.set_cell(2, 3, '#')
    assert grid.is_black(2, 3)


# Symmetry tests
def test_symmetry_enforced():
    """Test that symmetry automatically mirrors black squares."""
    grid = CrosswordGrid(5, enforce_symmetry=True)
    grid.set_black_square(0, 0)
    
    # Mirror at (4, 4) should automatically be black
    assert grid.is_black(4, 4)


def test_symmetry_not_enforced_by_default():
    """Test that symmetry is off by default."""
    grid = CrosswordGrid(5)
    grid.set_black_square(0, 0)
    
    # Mirror should NOT be black
    assert not grid.is_black(4, 4)


def test_check_symmetry_returns_true():
    """Test check_symmetry on symmetric grid."""
    grid = CrosswordGrid(5, enforce_symmetry=True)
    grid.set_black_square(0, 0)
    grid.set_black_square(1, 1)
    
    assert grid.check_symmetry() == True


def test_check_symmetry_returns_false():
    """Test check_symmetry on asymmetric grid."""
    grid = CrosswordGrid(5)
    grid.set_black_square(0, 0)
    
    assert grid.check_symmetry() == False


# Pattern generation tests
def test_generate_random_pattern():
    """Test that random pattern generates black squares."""
    grid = CrosswordGrid(15)
    grid.generate_pattern(method='random')
    
    # Should have some black squares
    assert grid.count_black_squares() > 0


def test_generate_random_pattern_with_symmetry():
    """Test that random pattern respects symmetry."""
    grid = CrosswordGrid(15, enforce_symmetry=True)
    grid.generate_pattern(method='random')
    
    # Should have black squares and be symmetric
    assert grid.count_black_squares() > 0
    assert grid.check_symmetry() == True


def test_generate_pattern_percentage():
    """Test that black_percentage parameter works approximately."""
    grid = CrosswordGrid(10)
    target_percentage = 0.20
    grid.generate_pattern(method='random', black_percentage=target_percentage)
    
    total_cells = 10 * 10
    actual_blacks = grid.count_black_squares()
    actual_percentage = actual_blacks / total_cells
    
    # Should be roughly 20% (within 10% tolerance due to randomness)
    assert 0.10 <= actual_percentage <= 0.30


# Validation tests
def test_invalid_size_too_small():
    """Test that grids smaller than MIN_SIZE raise error."""
    with pytest.raises(ValueError):
        CrosswordGrid(3)


def test_invalid_size_too_large():
    """Test that grids larger than MAX_SIZE raise error."""
    with pytest.raises(ValueError):
        CrosswordGrid(31)


def test_out_of_bounds_get():
    """Test that accessing out of bounds raises IndexError."""
    grid = CrosswordGrid(5)
    with pytest.raises(IndexError):
        grid.get_cell(5, 0)


def test_out_of_bounds_set():
    """Test that setting out of bounds raises IndexError."""
    grid = CrosswordGrid(5)
    with pytest.raises(IndexError):
        grid.set_cell(5, 0, '#')


# Helper method tests
def test_count_black_squares():
    """Test counting black squares."""
    grid = CrosswordGrid(5)
    grid.set_black_square(0, 0)
    grid.set_black_square(1, 1)
    grid.set_black_square(2, 2)
    
    assert grid.count_black_squares() == 3


def test_is_empty():
    """Test is_empty method."""
    grid = CrosswordGrid(5)
    assert grid.is_empty(0, 0) == True
    
    grid.set_black_square(0, 0)
    assert grid.is_empty(0, 0) == False


def test_is_filled():
    """Test is_filled method."""
    grid = CrosswordGrid(5)
    assert grid.is_filled(0, 0) == False
    
    grid.set_cell(0, 0, 'A')
    assert grid.is_filled(0, 0) == True
    
    grid.set_cell(1, 1, '#')
    assert grid.is_filled(1, 1) == False  # Black squares aren't "filled"

# tests/test_grid.py

def test_extract_slots_simple():
    """Test extracting slots from a simple grid."""
    grid = CrosswordGrid(5)
    # Create simple pattern: no black squares
    slots = grid.extract_slots()
    
    # Should have slots across and down
    across_slots = [s for s in slots if s.direction == 'across']
    down_slots = [s for s in slots if s.direction == 'down']
    
    assert len(across_slots) == 5  # One per row
    assert len(down_slots) == 5    # One per column


def test_extract_slots_with_blacks():
    """Test extracting slots with black squares."""
    grid = CrosswordGrid(5)
    grid.set_black_square(0, 2)  # Breaks first row
    
    slots = grid.extract_slots()
    
    # First row should now have 0 slots (segments too short: 2 letters each)
    first_row_across = [s for s in slots if s.row == 0 and s.direction == 'across']
    assert len(first_row_across) == 0  # Both segments < 3 letters


def test_calculate_overlaps():
    """Test calculating slot intersections."""
    grid = CrosswordGrid(5)
    slots = grid.extract_slots()
    overlaps = grid.calculate_overlaps(slots)
    
    # Should have overlaps (grid has no black squares, so all across/down cross)
    assert len(overlaps) > 0
    
    # Check an overlap exists
    across_slot = [s for s in slots if s.direction == 'across'][0]
    down_slot = [s for s in slots if s.direction == 'down'][0]
    
    # They should overlap if they're both in grid
    assert (across_slot, down_slot) in overlaps or (down_slot, across_slot) in overlaps


def test_slot_minimum_length():
    """Test that slots shorter than 3 letters are ignored."""
    grid = CrosswordGrid(5)
    # Create pattern with 2-letter gaps
    grid.set_black_square(0, 2)
    grid.set_black_square(0, 0)  # Leaves only 1 white square at (0,1)
    
    slots = grid.extract_slots()
    
    # No slot should have length < 3
    assert all(s.length >= 3 for s in slots)

def test_max_slot_length():
    """Test that max_slot_length is enforced."""
    grid = CrosswordGrid(15, enforce_symmetry=True)
    grid.generate_pattern(max_slot_length=8)
    
    max_length = grid.get_max_slot_length()
    assert max_length <= 8, f"Found slot with length {max_length}, expected <= 8"


def test_get_slot_length_stats():
    """Test slot length statistics."""
    grid = CrosswordGrid(10)
    grid.generate_pattern()
    
    stats = grid.get_slot_length_stats()
    assert stats['min'] >= 3  # Minimum slot length is 3
    assert stats['max'] > 0
    assert stats['avg'] > 0
    assert stats['count'] > 0