# Gridiculous! AC-3 powered crossword construction, with AI-assisted theming and clueing.

Deets: Themed puzzles using classic Constraint Satisfaction Problem (CSP) techniques...and room to grow into a full “constructor’s workbench” including LLM-assisted theme/clue tooling. When it's done it will supported alphanumeric entries and dynamic theme-based word scoring! 

## Overview
Generates crossword puzzles using:
- AC-3 constraint propagation algorithm
- Backtracking search
- Theme word placement and scoring
- Automatic clue generation
- Support for letters and digits in the answers  

# Basic generation
python scripts/generate.py --output my_puzzle.json

# With theme
python scripts/generate.py \
  --theme "Space Exploration" \
  --theme-words "ASTRONAUT,SPACECRAFT" \
  --size 15 \
  --output space_puzzle.json

# From theme file
python scripts/generate.py \
  --theme-file data/examples/themes/ai_theme.json \
  --output ai_puzzle.json

## Project Structure

```
crossword-generator/
├── README.md                   # Project overview and quick start
├── requirements.txt            # Python dependencies
├── setup.py                    # Package installation (optional)
│
├── data/                       # Word lists and resources
│   ├── word_lists/
│   │   ├── enable.txt         # Main word list (download on setup)
│   │   └── common_words.txt   # Curated high-quality words (optional)
│   └── examples/
│       ├── grids/             # Example grid patterns
│       └── themes/            # Example theme configurations
│
├── src/                        # Main source code
│   ├── __init__.py
│   ├── grid.py                # Grid creation & black square placement
│   ├── solver.py              # CSP solver (AC-3 + backtracking)
│   ├── theme.py               # Theme word placement & scoring
│   ├── clues.py               # Clue metadata generation
│   └── utils.py               # Helper functions
│
├── scripts/                    # Standalone scripts
│   ├── download_wordlist.py   # Setup: download word lists
│   └── generate.py            # CLI tool to generate puzzles
│
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── test_grid.py
│   ├── test_solver.py
│   └── test_theme.py
│
└── output/                     # Generated puzzles (gitignored)
    ├── .gitkeep
    └── examples/              # Example outputs (committed)
        └── sample_puzzle.json
```

 
## License
MIT License

## Quick Start

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd crossword-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download word lists:
```bash
python scripts/download_wordlist.py
```

### Usage

Generate a crossword puzzle:
```bash
python scripts/generate.py --width 15 --height 15 --output output/puzzle.json
```

Generate with theme words:
```bash
python scripts/generate.py --width 15 --height 15 --theme PYTHON CODING AI --output output/puzzle.json
```

### Running Tests

```bash
python -m pytest tests/
```

Or using unittest:
```bash
python -m unittest discover tests
```