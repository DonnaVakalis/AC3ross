"""
Unit tests for solver.py
"""

import unittest
from src.solver import ac3, backtrack_search, solve_crossword


class TestSolver(unittest.TestCase):
    """Test cases for CSP solver"""
    
    def test_ac3(self):
        """Test AC-3 algorithm"""
        constraints = []
        domains = {}
        result = ac3(constraints, domains)
        self.assertIsInstance(result, bool)
    
    def test_backtrack_search(self):
        """Test backtracking search"""
        assignment = {}
        csp = {}
        result = backtrack_search(assignment, csp)
        self.assertIsNotNone(result)
    
    def test_solve_crossword(self):
        """Test crossword solving"""
        grid = [[None] * 5 for _ in range(5)]
        word_list = ["HELLO", "WORLD"]
        result = solve_crossword(grid, word_list)
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main()

