import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.theme import ThemeManager
from src.grid import CrosswordGrid
from src.solver import CrosswordSolver
from src.utils import load_word_list

# Load pre-scored list
theme = ThemeManager.load_from_file('data/scored_lists/ai_ml_scored.json')

print(f"Loaded theme: {theme.description}")
print(f"Loaded {len(theme.word_scores)} scored words")

# Use in solving
grid = CrosswordGrid(9, enforce_symmetry=True)
grid.generate_pattern()

slots = grid.extract_slots()
overlaps = grid.calculate_overlaps(slots)
words = load_word_list()

solver = CrosswordSolver(slots, words, overlaps, theme=theme)
solution = solver.solve()