"""
Add more scores to an existing list
"""
import sys
from pathlib import Path

# Add project root to Python path so we can import src
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    

from src.theme import ThemeManager
from src.llm_scorer import LLMWordScorer

# Load existing
theme = ThemeManager.load_from_file('data/scored_lists/ai_ml_scored.json')

# Score additional words
scorer = LLMWordScorer()
new_words = ["TRANSFORMER", "BACKPROP", "GRADIENT"]
new_scores = scorer.score_words_batch(new_words, theme.description)

# Add to theme
for word, score in new_scores.items():
    theme.set_word_score(word, score)

# Save updated list
theme.save_scores('data/scored_lists/ai_ml_scored.json')