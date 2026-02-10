# Scored Word Lists

This directory contains pre-scored word lists for different themes.

## File Format

Each `.json` file contains:
- **metadata**: Theme info, scoring date, model used
- **scores**: Word -> score (0-100) mapping

 
## Creating New Scored Lists

### Option 1: Use LLM Scorer
```python
from src.llm_scorer import LLMWordScorer
from src.utils import load_word_list

words = load_word_list()[:1000]
scorer = LLMWordScorer()
scorer.score_and_save(
    words,
    "Your Theme Here",
    "data/scored_lists/your_theme_scored.json"
)
```

### Option 2: Manual Scoring
```python
from src.theme import ThemeManager

theme = ThemeManager(description="Your Theme")
theme.set_word_score("WORD1", 85.0)
theme.set_word_score("WORD2", 70.0)
theme.save_scores("data/scored_lists/your_theme_scored.json")
```

## Loading Scored Lists
```python
from src.theme import ThemeManager

# Load single list
theme = ThemeManager.load_from_file('data/scored_lists/ai_ml_scored.json')

# Merge multiple lists
theme = ThemeManager(description="Combined")
theme.merge_scored_lists([
    'data/scored_lists/ai_ml_scored.json',
    'data/scored_lists/space_scored.json'
], strategy='max')
```

## Sharing Scored Lists

Scored lists are JSON files that can be:
- Committed to git (they're text files)
- Shared with others
- Combined/merged
- Version controlled

Feel free to create and share your own themed scored lists!