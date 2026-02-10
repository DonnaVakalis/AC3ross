 
"""Quick check of the solver on a small grid."""

import sys
from pathlib import Path

# Add project root to Python path so we can import src
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.grid import CrosswordGrid
from src.solver import CrosswordSolver
from src.utils import load_word_list


# Create small grid
grid = CrosswordGrid(7, enforce_symmetry=True)
grid.generate_pattern(max_slot_length=7)

print("Grid pattern:")
print(grid)
print()

grid.print_grid_info()
print()

# Extract slots
slots = grid.extract_slots()
overlaps = grid.calculate_overlaps(slots)

# Load words
print("Loading word list...")
words = load_word_list()
print()

# Solve!
solver = CrosswordSolver(slots, words, overlaps)
solution = solver.solve()

if solution:
    print("\n" + "="*50)
    print("SOLUTION FOUND!")
    print("="*50)
    
    # Fill grid
    for slot, word in solution.items():
        for i, (row, col) in enumerate(slot.cells):
            grid.set_cell(row, col, word[i])
    
    print()
    grid.visualize_filled()
else:
    print("\nNo solution found :(")