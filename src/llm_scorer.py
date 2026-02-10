"""LLM-based word scoring for theme relevance."""

import json
from typing import List, Dict, Optional
from anthropic import Anthropic

"""LLM-based word scoring for theme relevance."""

import json
import requests
from typing import List, Dict, Optional, Literal
from anthropic import Anthropic


class LLMWordScorer:
    """
    Score words for theme relevance using LLMs.
    
    Supports:
    - Claude (via Anthropic API) - paid
    - Local models (via Ollama) - free
    """
    
    def __init__(self, 
                 provider: Literal["claude", "ollama"] = "claude",
                 api_key: Optional[str] = None,
                 model: str = None,
                 ollama_base_url: str = "http://localhost:11434"):
        """
        Initialize LLM scorer.
        
        Args:
            provider: "claude" or "ollama"
            api_key: Anthropic API key (only for provider="claude")
            model: Model name
                - For claude: "claude-sonnet-4-20250514" (default)
                - For ollama: "llama3.1", "mistral", "qwen2.5" etc.
            ollama_base_url: Ollama server URL (default: localhost)
        
        Examples:
            # Use Claude
            >>> scorer = LLMWordScorer(provider="claude")
            
            # Use local Ollama
            >>> scorer = LLMWordScorer(provider="ollama", model="llama3.1")
        """
        self.provider = provider
        self.ollama_base_url = ollama_base_url
        
        if provider == "claude":
            self.client = Anthropic(api_key=api_key)
            self.model = model or "claude-sonnet-4-20250514"
        elif provider == "ollama":
            self.client = None
            self.model = model or "llama3.1"  # Default to Llama 3.1
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def score_words_batch(self, 
                         words: List[str], 
                         theme_description: str,
                         batch_size: int = 100,
                         max_batches: Optional[int] = None) -> Dict[str, float]:
        """
        Score a list of words for theme relevance in batches.
        
        Args:
            words: List of words to score
            theme_description: Description of the theme
            batch_size: Number of words per API call
            max_batches: Maximum number of batches to process
        
        Returns:
            Dictionary mapping words to scores (0-100)
        """
        # Adjust batch size for Ollama (smaller batches work better)
        if self.provider == "ollama":
            batch_size = min(batch_size, 50)  # Smaller batches for local models
        
        all_scores = {}
        
        # Process in batches
        for i in range(0, len(words), batch_size):
            batch_num = i // batch_size
            if max_batches and batch_num >= max_batches:
                print(f"Reached max_batches limit ({max_batches})")
                break
            
            batch = words[i:i+batch_size]
            
            print(f"Scoring batch {batch_num + 1} ({len(batch)} words)...")
            
            try:
                batch_scores = self._score_single_batch(batch, theme_description)
                all_scores.update(batch_scores)
                
                print(f"  ✓ Scored {len(batch_scores)} words")
                
            except Exception as e:
                print(f"  ✗ Error scoring batch: {e}")
                continue
        
        print(f"\nTotal scored: {len(all_scores)} words")
        return all_scores
    
    def _score_single_batch(self, words: List[str], theme_description: str) -> Dict[str, float]:
        """Score a single batch using the configured provider."""
        if self.provider == "claude":
            return self._score_with_claude(words, theme_description)
        elif self.provider == "ollama":
            return self._score_with_ollama(words, theme_description)
    
    def _score_with_claude(self, words: List[str], theme_description: str) -> Dict[str, float]:
        """Score using Claude API."""
        prompt = self._create_scoring_prompt(words, theme_description)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        response_text = response.content[0].text
        scores = self._parse_scores(response_text, words)
        
        return scores
    
    def _score_with_ollama(self, words: List[str], theme_description: str) -> Dict[str, float]:
        """Score using local Ollama model."""
        prompt = self._create_scoring_prompt(words, theme_description)
        
        # Call Ollama API
        response = requests.post(
            f"{self.ollama_base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower temperature for more consistent scoring
                    "num_predict": 2000  # Max tokens
                }
            },
            timeout=120  # 2 minute timeout
        )
        
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code} {response.text}")
        
        response_text = response.json()["response"]
        scores = self._parse_scores(response_text, words)
        
        return scores
    
    def _create_scoring_prompt(self, words: List[str], theme_description: str) -> str:
        """Create prompt for word scoring."""
        words_list = '\n'.join(words)
        
        prompt = f"""You are helping create a themed crossword puzzle. The theme is: "{theme_description}"

        Score each word below for how relevant it is to this theme on a scale of 0-100:
        - 0 = Completely unrelated to the theme
        - 25 = Tangentially related
        - 50 = Moderately related
        - 75 = Strongly related
        - 100 = Core concept of the theme

        Be generous with scoring - even indirect connections count. For example:
        - For "Space Exploration": ROCKET=95, ASTRONAUT=95, GRAVITY=80, SCIENCE=60, TRAVEL=40, DISCOVER=30
        - For "Cooking": RECIPE=100, KITCHEN=90, HEAT=70, KNIFE=85, TIMER=75, MEASURE=60

        Words to score:
        {words_list}

        Respond with ONLY a JSON object mapping each word to its score. No explanation needed.
        Format: {{"WORD1": score, "WORD2": score, ...}}

        JSON:"""
        
        return prompt
    
    def _parse_scores(self, response_text: str, words: List[str]) -> Dict[str, float]:
        """Parse LLM response into word scores."""
        try:
            # Extract JSON from response
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                json_text = response_text[json_start:json_end].strip()
            elif '```' in response_text:
                json_start = response_text.find('```') + 3
                json_end = response_text.find('```', json_start)
                json_text = response_text[json_start:json_end].strip()
            elif '{' in response_text and '}' in response_text:
                # Find first { and last }
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text.strip()
            
            # Parse JSON
            scores = json.loads(json_text)
            
            # Validate and convert to float
            validated_scores = {}
            for word in words:
                if word in scores:
                    score = float(scores[word])
                    # Clamp to 0-100
                    score = max(0.0, min(100.0, score))
                    validated_scores[word] = score
                else:
                    # Word not in response, default to 0
                    validated_scores[word] = 0.0
            
            return validated_scores
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Response: {response_text[:200]}...")
            # Return default scores
            return {word: 0.0 for word in words}
    
    def score_and_save(self,
                      words: List[str],
                      theme_description: str,
                      output_path: str,
                      batch_size: int = 100,
                      max_batches: Optional[int] = None):
        """
        Score words and save directly to file.
        
        Args:
            words: Words to score
            theme_description: Theme description
            output_path: Where to save (e.g., 'data/scored_lists/ai_scored.json')
            batch_size: Batch size
            max_batches: Max batches to process
        
        Example:
            >>> scorer = LLMWordScorer()
            >>> words = load_word_list()[:1000]
            >>> scorer.score_and_save(
            ...     words,
            ...     "Artificial Intelligence",
            ...     "data/scored_lists/ai_ml_scored.json"
            ... )
        """
        # Score words
        scores = self.score_words_batch(
            words, theme_description, 
            batch_size=batch_size,
            max_batches=max_batches
        )
        
        # Create theme and save
        theme = ThemeManager(description=theme_description)
        for word, score in scores.items():
            theme.set_word_score(word, score)
        
        theme.save_scores(
            output_path,
            metadata={
                'model_used': self.model,
                'scoring_method': 'llm_batch',
                'batch_size': batch_size
            }
        )
        
        return theme
     
    def score_words_smart(self,
                         words: List[str],
                         theme_description: str,
                         target_scored_words: int = 1000) -> Dict[str, float]:
        """
        Smart scoring strategy: Score most likely relevant words first.
        
        Uses heuristics to identify potentially relevant words, then scores those.
        More efficient than scoring entire word list.
        
        Args:
            words: Full word list
            theme_description: Theme description
            target_scored_words: How many words to score (default 1000)
        
        Returns:
            Dictionary of scored words
        
        Strategy:
            1. Extract keywords from theme
            2. Filter words that contain theme keywords
            3. Score those words with LLM
            4. Remaining words default to 0
        """
        # Extract theme keywords (much too simple approach but need to start somewhere !:))
        theme_keywords = self._extract_theme_keywords(theme_description)
        
        # Filter potentially relevant words
        candidate_words = []
        for word in words:
            word_upper = word.upper()
            for keyword in theme_keywords:
                if keyword in word_upper or word_upper in keyword:
                    candidate_words.append(word)
                    break
        
        # Limit to target number
        candidate_words = candidate_words[:target_scored_words]
        
        print(f"Found {len(candidate_words)} candidate words containing theme keywords")
        print(f"Scoring with LLM...")
        
        # Score candidates
        scores = self.score_words_batch(candidate_words, theme_description)
        
        return scores
    
    def _extract_theme_keywords(self, theme_description: str) -> List[str]:
        """
        Extract keywords from theme description.
        
        Simple approach: split on spaces, remove common words.
        
        Args:
            theme_description: Theme description
        
        Returns:
            List of keywords (uppercase)
        """
        # Common words to ignore
        stop_words = {'THE', 'A', 'AN', 'AND', 'OR', 'BUT', 'IN', 'ON', 'AT', 'TO', 'FOR'}
        
        words = theme_description.upper().split()
        keywords = [w for w in words if w not in stop_words and len(w) >= 3]
        
        return keywords