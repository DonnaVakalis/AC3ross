"""
Basic crossword solving example (no theme).

- Creating a grid
- Generating a pattern
- Loading words
- Creating the puzzle grid
"""
import sys
from pathlib import Path

# Add project root to Python path so we can import src
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    
from src.grid import CrosswordGrid
from src.solver import CrosswordSolver
from src.utils import load_word_list

def main():
    print("="*60)
    print("Basic Crossword Solver Example")
    print("="*60)
    
    # 1. Create grid
    print("\n1. Creating 7x7 grid with symmetry...")
    grid = CrosswordGrid(7, enforce_symmetry=True)
    grid.generate_pattern(max_slot_length=7)
    
    print(grid)
    grid.print_grid_info()
    
    # 2. Extract slots
    print("\n2. Extracting word slots...")
    slots = grid.extract_slots()
    overlaps = grid.calculate_overlaps(slots)
    
    # 3. Load word list
    print("\n3. Loading word list...")
    words = load_word_list()
    
    # 4. Solve
    print("\n4. Solving puzzle...")
    solver = CrosswordSolver(slots, words, overlaps)
    solution = solver.solve()
    
    # 5. Display result
    if solution:
        print("\n" + "="*60)
        print("SOLUTION FOUND!")
        print("="*60)
        
        # Fill grid with solution
        for slot, word in solution.items():
            for i, (row, col) in enumerate(slot.cells):
                grid.set_cell(row, col, word[i])
        
        print()
        grid.visualize_filled()
        
        print("\nSlot assignments:")
        for slot, word in sorted(solution.items(), key=lambda x: (x[0].row, x[0].col)):
            print(f"  {slot}: {word}")
    else:
        print("\n✗ No solution found")

if __name__ == "__main__":
    main()