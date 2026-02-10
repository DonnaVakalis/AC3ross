# Word Lists

## Base List
- `enable.txt` - ENABLE word list (~173k words)
  - Downloaded via `python scripts/download_wordlist.py`
  - Single words only, no phrases

## Custom Lists (add your own!)
- `custom_phrases.txt` - Multi-word phrases (IMONIT, LETITGO)
- `custom_numeric.txt` - Alphanumeric entries (314, CO2, H2O)
- `custom_theme_*.txt` - Theme-specific vocabularies

## Creating Custom Lists
1. Create a text file with one word per line
2. Use UPPERCASE
3. No spaces within entries (IMONIT not I'M ON IT)

See `scripts/create_custom_wordlist_example.py` for examples.

## Loading
```python
from src.utils import load_word_list

# Base only
words = load_word_list()

# With custom lists
words = load_word_list(
    custom_lists=['data/word_lists/custom_phrases.txt']
)
```
```

---

## Summary: File Structure
```
xword_gen/
├── data/
│   └── word_lists/
│       ├── README.md                    # ← Explains system
│       ├── enable.txt                   # Base (downloaded)
│       ├── custom_phrases.txt           # Your multi-word
│       ├── custom_numeric.txt           # Your alphanumeric
│       └── custom_theme_ai.txt          # Theme-specific
│
├── scripts/
│   ├── download_wordlist.py
│   └── create_custom_wordlist_example.py  # ← Shows how
│
└── src/
    └── utils.py                         # load_word_list() handles merging