 
import sys
from pathlib import Path

# Add project root to Python path so we can import src
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.llm_scorer import LLMWordScorer
from src.utils import load_word_list

# Load words
words = load_word_list()

# Score for AI theme
scorer = LLMWordScorer()
theme = scorer.score_and_save(
    words[:1000],  # Score first 1000 words
    theme_description="Artificial Intelligence and Machine Learning",
    output_path="data/scored_lists/ai_ml_scored.json",
    batch_size=100
)

print("Done! Scored list saved.")