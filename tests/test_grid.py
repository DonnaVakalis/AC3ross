"""
Unit tests for grid.py
"""

import unittest
from src.grid import create_grid, place_black_squares


class TestGrid(unittest.TestCase):
    """Test cases for grid creation and black square placement"""
    
    def test_create_grid(self):
        """Test grid creation"""
        grid = create_grid(5, 5)
        self.assertEqual(len(grid), 5)
        self.assertEqual(len(grid[0]), 5)
    
    def test_place_black_squares(self):
        """Test black square placement"""
        grid = create_grid(5, 5)
        result = place_black_squares(grid)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()

