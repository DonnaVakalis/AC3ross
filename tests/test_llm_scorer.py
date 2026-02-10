import pytest
import requests
from src.llm_scorer import LLMWordScorer

def is_ollama_running():
    """Check if Ollama is running."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        print("Ollama not running. Install: curl -fsSL https://ollama.com/install.sh | sh")
        return False


@pytest.mark.skipif(not is_ollama_running(), reason="Ollama not running")
def test_score_with_ollama():
    """Test scoring with Ollama (only if Ollama is running)."""
    scorer = LLMWordScorer(provider="ollama", model="llama3.1")
    
    words = ["ROBOT", "NEURAL", "TREE", "BEACH"]
    scores = scorer.score_words_batch(words, "Artificial Intelligence", batch_size=4)
    
    # AI words should score higher
    assert scores["ROBOT"] > scores["BEACH"]
    assert scores["NEURAL"] > scores["TREE"]
    
    print(f"\nScores: {scores}")


@pytest.mark.skip(reason="Requires Claude API key and makes real API calls")
def test_score_with_claude():
    """Test scoring with Claude (skipped by default to avoid API costs)."""
    scorer = LLMWordScorer(provider="claude")
    
    words = ["ROBOT", "NEURAL", "ALGORITHM", "TREE", "DOG", "BEACH"]
    theme = "Artificial Intelligence"
    
    scores = scorer.score_words_batch(words, theme, batch_size=6)
    
    # AI-related words should score higher
    assert scores["ROBOT"] > scores["BEACH"]
    assert scores["NEURAL"] > scores["DOG"]
    assert scores["ALGORITHM"] > scores["TREE"]


def test_extract_theme_keywords():
    """Test keyword extraction from theme."""
    scorer = LLMWordScorer(provider="ollama")  # Provider doesn't matter for this test
    
    keywords = scorer._extract_theme_keywords("Space Exploration and Astronomy")
    
    assert "SPACE" in keywords
    assert "EXPLORATION" in keywords
    assert "ASTRONOMY" in keywords
    assert "AND" not in keywords  # Stop word