"""
Crossword Puzzle Solver using Constraint Satisfaction Problem (CSP) Algorithms

This module solves crossword puzzles by treating them as a Constraint Satisfaction Problem.
Instead of brute-force trying every word combination, it uses intelligent algorithms to
efficiently find valid word placements.

HOW IT WORKS:
-------------
1. **Problem Setup**: 
   - Slots (empty word positions) are the "variables" to fill
   - Word list provides the "values" (possible words)
   - Overlaps between slots create "constraints" (matching letters)

2. **AC-3 Algorithm (Arc Consistency)**:
   - Before searching, removes impossible words from each slot's domain
   - If slot A overlaps with slot B at position 3, only words with matching
     letters at those positions are kept
   - Prunes the search space dramatically before backtracking begins

3. **Backtracking Search**:
   - Systematically tries word assignments, backtracking when conflicts occur
   - Uses heuristics to be smarter than naive search:
     * **MRV (Minimum Remaining Values)**: Fill slots with fewest options first
     * **LCV (Least Constraining Value)**: Try words that eliminate fewest 
       options from neighboring slots first

USAGE:
------
    >>> from src.grid import CrosswordGrid
    >>> from src.utils import load_word_list
    >>> 
    >>> # Create grid and extract slots
    >>> grid = CrosswordGrid(15, 15)
    >>> slots = grid.extract_slots()
    >>> overlaps = grid.calculate_overlaps(slots)
    >>> 
    >>> # Load words and solve
    >>> words = load_word_list()
    >>> solver = CrosswordSolver(slots, words, overlaps)
    >>> solution = solver.solve()
    >>> 
    >>> # solution is a dict: {slot: "WORD"}

KEY CONCEPTS:
-------------
- **CSP**: A problem where variables must be assigned values while satisfying constraints
- **Domain**: The set of possible values (words) for each variable (slot)
- **Arc Consistency**: When two variables overlap, their domains must be compatible
- **Backtracking**: Recursive search that undoes bad choices and tries alternatives
"""
import sys
from pathlib import Path

# Add project root to Python path so we can import src
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from typing import List, Dict, Set, Tuple, Optional
from src.grid import Slot
from src.utils import words_by_length


class CrosswordSolver:
    """
    Solves crossword puzzles using Constraint Satisfaction Problem (CSP) algorithms.
    
    Uses:
    - Node consistency: Filter words by slot length
    - AC-3: Arc consistency for constraint propagation
    - Backtracking: Search with MRV and LCV heuristics
    """
    
    def __init__(self, 
                 slots: List[Slot], 
                 word_list: List[str], 
                 overlaps: Dict,
                 theme: Optional['ThemeManager'] = None,
                 theme_assignment: Optional[Dict[Slot, str]] = None,
                 theme_influence: float = 1.0):        
        """
        Initialize the crossword solver.
        
        Args:
            slots: List of Slot objects to fill
            word_list: List of available words (uppercase)
            overlaps: Dictionary mapping (slot1, slot2) -> (index1, index2)
            theme: ThemeManager instance (optional) for theme-aware solving
            theme_assignment: Dictionary pre-mapping slots to theme words (optional)
            theme_influence:  How strongly to prefer high-scored words (0.0-10.0)
                0.0 = ignore scores completely (pure LCV)
                1.0 = balanced influence (default)
                5.0 = strong preference for high-scored words
                10.0 = extreme preference for high-scored words
        Example:
            >>> slots = grid.extract_slots()
            >>> overlaps = grid.calculate_overlaps(slots)
            >>> words = load_word_list()
            >>> solver = CrosswordSolver(slots, words, overlaps)
            >>> solution = solver.solve()
        """
        self.slots = slots
        self.overlaps = overlaps
        self.theme = theme
        self.theme_influence = theme_influence 
        
        # Organize words by length for fast lookup
        self.words_by_len = words_by_length(word_list)
        
        # Initialize domains: possible words for each slot
        self.domains = self._initialize_domains()
        
        # If provided, pre-assign theme words
        self.theme_assignment = theme_assignment or {}
        if self.theme_assignment:
            self._apply_theme_assignment()

        # Track statistics
        self.backtrack_count = 0
        self.ac3_count = 0
    
    def _apply_theme_assignment(self):
        """
        Apply pre-assigned theme words as hard constraints.
        
        For each theme word assignment:
        1. Lock that slot to only that word
        2. Constrain overlapping slots based on theme word letters
        """
        for slot, theme_word in self.theme_assignment.items():
            # Lock this slot to the theme word
            self.domains[slot] = {theme_word}
            
            # Constrain overlapping slots
            for other_slot in self.slots:
                if other_slot in self.theme_assignment:
                    continue  # Skip other theme slots
                
                if (slot, other_slot) not in self.overlaps:
                    continue
                
                idx1, idx2 = self.overlaps[(slot, other_slot)]
                required_letter = theme_word[idx1]
                
                # Filter other_slot's domain to only words with matching letter
                self.domains[other_slot] = {
                    w for w in self.domains[other_slot]
                    if w[idx2] == required_letter
                }
    
    def _order_domain_values(self, slot: Slot, assignment: Dict[Slot, str]) -> List[str]:
        """
        Order values for slot using LCV heuristic + theme scoring.
        
        Uses self.theme_influence to control how much theme scores matter.
        """
        
        def score_word(word):
            """
            Score word for ordering.
            
            Lower score = higher priority (tried first).
            
            Combines:
            - Conflict count (LCV - fewer conflicts = lower score)
            - Theme score (higher theme relevance = lower final score)
            - Theme influence (controls how much theme score matters)
            """
            # Count conflicts (LCV heuristic)
            conflicts = 0
            for neighbor in self.slots:
                if neighbor in assignment:
                    continue
                
                if (slot, neighbor) not in self.overlaps:
                    continue
                
                idx1, idx2 = self.overlaps[(slot, neighbor)]
                
                for neighbor_word in self.domains[neighbor]:
                    if word[idx1] != neighbor_word[idx2]:
                        conflicts += 1
            
            # Get theme score (0-100, higher = more relevant)
            theme_score = 0.0
            if self.theme:
                theme_score = self.theme.get_word_score(word)
            
            # Turn up/down the influence knob 
            theme_bonus = (theme_score / 100.0) * conflicts * self.theme_influence
            
            return conflicts - theme_bonus
        
        # Get valid words
        words = [w for w in self.domains[slot] 
                if self._is_consistent(slot, w, assignment)]
        
        # Sort by combined score
        words.sort(key=score_word)
        
        return words










    def _initialize_domains(self) -> Dict[Slot, Set[str]]:
        """
        Initialize domain for each slot (node consistency).
        
        Returns:
            Dictionary mapping each slot to its set of possible words
        
        Node consistency: Only include words that match the slot length.
        """
        domains = {}
        
        for slot in self.slots:
            # Get all words of the correct length
            if slot.length in self.words_by_len:
                domains[slot] = self.words_by_len[slot.length].copy()
            else:
                domains[slot] = set()  # No words of this length
            
            if not domains[slot]:
                print(f"Warning: No words found for slot {slot} (length {slot.length})")
        
        return domains
    
    def solve(self) -> Optional[Dict[Slot, str]]:
        """
        Solve the crossword puzzle.
        
        Returns:
            Dictionary mapping slots to words (solution), or None if no solution exists
        
        Algorithm:
            1. Enforce arc consistency (AC-3)
            2. Backtracking search with heuristics
        """
        print(f"Starting solve with {len(self.slots)} slots...")
        
        # Step 1: Enforce arc consistency
        print("Running AC-3...")
        if not self.ac3():
            print("AC-3 failed - puzzle has no solution")
            return None
        
        print(f"AC-3 complete. Starting backtracking search...")
        
        # Step 2: Backtracking search
        self.backtrack_count = 0
        assignment = {}
        solution = self.backtrack(assignment)
        
        if solution:
            print(f"✓ Solution found after {self.backtrack_count} backtracks")
        else:
            print(f"✗ No solution found after {self.backtrack_count} backtracks")
        
        return solution
    
    def ac3(self) -> bool:
        """
        AC-3 algorithm for arc consistency.
        
        Returns:
            True if arc consistency achieved, False if inconsistency detected
        
        This prunes impossible values from domains before search begins.
        """
        # Create queue of all arcs (slot pairs that overlap)
        queue = list(self.overlaps.keys())
        
        while queue:
            slot1, slot2 = queue.pop(0)
            
            # Revise domain of slot1 based on slot2
            if self._revise(slot1, slot2):
                # Domain of slot1 was reduced
                
                # Check if domain is now empty (no solution possible)
                if not self.domains[slot1]:
                    return False
                
                # Add all neighbors of slot1 back to queue (except slot2)
                for slot in self.slots:
                    if slot != slot1 and slot != slot2:
                        if (slot, slot1) in self.overlaps:
                            queue.append((slot, slot1))
        
        return True
    
    def _revise(self, slot1: Slot, slot2: Slot) -> bool:
        """
        Revise domain of slot1 based on constraint with slot2.
        
        Args:
            slot1: Slot whose domain we're revising
            slot2: Slot that constrains slot1
        
        Returns:
            True if domain of slot1 was revised (reduced), False otherwise
        """
        revised = False
        
        # Get overlap position
        if (slot1, slot2) not in self.overlaps:
            return False
        
        idx1, idx2 = self.overlaps[(slot1, slot2)]
        
        # Check each word in slot1's domain
        to_remove = set()
        for word1 in self.domains[slot1]:
            # Check if there exists a word in slot2's domain that's compatible
            compatible = False
            for word2 in self.domains[slot2]:
                # Compatible if letters at overlap position match
                if word1[idx1] == word2[idx2]:
                    compatible = True
                    break
            
            # If no compatible word in slot2, remove word1 from slot1's domain
            if not compatible:
                to_remove.add(word1)
                revised = True
        
        # Remove incompatible words
        self.domains[slot1] -= to_remove
        
        return revised
    
    def backtrack(self, assignment: Dict[Slot, str]) -> Optional[Dict[Slot, str]]:
        """
        Backtracking search with heuristics.
        
        Args:
            assignment: Current partial assignment of slots to words
        
        Returns:
            Complete assignment (solution) or None if no solution
        """
        self.backtrack_count += 1
        
        # Check if assignment is complete
        if len(assignment) == len(self.slots):
            return assignment
        
        # Select unassigned slot using MRV heuristic
        slot = self._select_unassigned_slot(assignment)
        
        # Try values in order of LCV heuristic
        for word in self._order_domain_values(slot, assignment):
            # Check if assignment is consistent
            if self._is_consistent(slot, word, assignment):
                # Add to assignment
                assignment[slot] = word
                
                # Recurse
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                
                # Backtrack
                del assignment[slot]
        
        return None
    
    def _select_unassigned_slot(self, assignment: Dict[Slot, str]) -> Slot:
        """
        Select next slot to assign using MRV (Minimum Remaining Values) heuristic.
        
        Args:
            assignment: Current partial assignment
        
        Returns:
            Unassigned slot with smallest domain (fewest possible words)
        
        Tie-breaking: Choose slot with most overlaps (degree heuristic)
        """
        unassigned = [s for s in self.slots if s not in assignment]
        
        # MRV: Pick slot with fewest remaining values
        def slot_priority(slot):
            # Count remaining valid words for this slot
            valid_words = len([w for w in self.domains[slot] 
                              if self._is_consistent(slot, w, assignment)])
            
            # Count overlaps (degree) - negative for tie-breaking (more overlaps = higher priority)
            overlaps_count = sum(1 for s in self.slots 
                                if (slot, s) in self.overlaps)
            
            return (valid_words, -overlaps_count)
        
        return min(unassigned, key=slot_priority)
    
    def _order_domain_values(self, slot: Slot, assignment: Dict[Slot, str]) -> List[str]:
        """
        Order values for slot using LCV (Least Constraining Value) heuristic.
        
        Args:
            slot: Slot to assign
            assignment: Current partial assignment
        
        Returns:
            List of words ordered by how many options they eliminate in neighbors
        
        LCV: Try words that eliminate fewest options from neighboring slots first.
        """
        def count_conflicts(word):
            """Count how many options this word eliminates in neighbors."""
            conflicts = 0
            
            # Check each neighboring slot
            for neighbor in self.slots:
                if neighbor in assignment:
                    continue
                
                if (slot, neighbor) not in self.overlaps:
                    continue
                
                idx1, idx2 = self.overlaps[(slot, neighbor)]
                
                # Count words in neighbor's domain that would be eliminated
                for neighbor_word in self.domains[neighbor]:
                    if word[idx1] != neighbor_word[idx2]:
                        conflicts += 1
            
            return conflicts
        
        # Sort words by conflict count (ascending - least conflicts first)
        words = [w for w in self.domains[slot] 
                if self._is_consistent(slot, w, assignment)]
        words.sort(key=count_conflicts)
        
        return words
    
    def _is_consistent(self, slot: Slot, word: str, assignment: Dict[Slot, str]) -> bool:
        """
        Check if assigning word to slot is consistent with current assignment.
        
        Args:
            slot: Slot to assign
            word: Word to assign to slot
            assignment: Current partial assignment
        
        Returns:
            True if consistent, False otherwise
        """
        # Check all overlapping slots
        for other_slot in self.slots:
            if other_slot not in assignment:
                continue
            
            if (slot, other_slot) not in self.overlaps:
                continue
            
            # Get overlap positions
            idx1, idx2 = self.overlaps[(slot, other_slot)]
            other_word = assignment[other_slot]
            
            # Check if letters match at overlap
            if word[idx1] != other_word[idx2]:
                return False
        
        return True