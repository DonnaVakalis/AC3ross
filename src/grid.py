"""
Grid creation & black square placement
"""

class CrosswordGrid:
    """
    Represents a crossword puzzle grid.
    
    Grid cells can contain:
    - None: empty white square (not yet filled)
    - '#': black square (blocked)
    - Any single character: filled cell (letter or digit)
    """
    MIN_SIZE = 4
    MAX_SIZE = 30
    BLACK_SQUARE = '#'
 

    def __init__(self, width, height=None, enforce_symmetry=False):
        """
        Args:
            width: Grid width
            height: Grid height (defaults to width for square)
            enforce_symmetry: If True, enforce 180° rotational symmetry
        
        Raises:
            ValueError: If dimensions are out of valid range
        """
        if height is None:
            height = width

        # Validate dimensions  
        if not (self.MIN_SIZE <= width <= self.MAX_SIZE):
            raise ValueError(f"Width must be between {self.MIN_SIZE} and {self.MAX_SIZE}")
        if not (self.MIN_SIZE <= height <= self.MAX_SIZE):
            raise ValueError(f"Height must be between {self.MIN_SIZE} and {self.MAX_SIZE}")
       
        
        self.width = width
        self.height = height
        self.enforce_symmetry = enforce_symmetry
        self.grid = [[None] * width for _ in range(height)]
    
    def get_cell(self, row, col):
        """
        Get the value at a specific cell.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
        
        Returns:
            Cell value (None, '#', or character)
        
        Raises:
            IndexError: If row or col out of bounds
        """
        if not (0 <= row < self.height and 0 <= col < self.width):
            raise IndexError(f"Cell ({row},{col}) out of bounds")
        
        return self.grid[row][col]
    
    def is_black(self, row, col):
        """Check if a cell is a black square."""
        return self.get_cell(row, col) == self.BLACK_SQUARE
    
    def is_empty(self, row, col):
        """Check if a cell is empty (not filled yet)."""
        return self.get_cell(row, col) is None
    
    def is_filled(self, row, col):
        """Check if a cell is filled with a character."""
        cell = self.get_cell(row, col)
        return cell is not None and cell != self.BLACK_SQUARE
    
    def count_black_squares(self):
        """Count total number of black squares in grid."""
        return sum(1 for row in self.grid 
                     for cell in row 
                     if cell == self.BLACK_SQUARE)
    
    def count_empty_squares(self):
        """Count total number of empty (unfilled) squares."""
        return sum(1 for row in self.grid 
                     for cell in row 
                     if cell is None)
    

    def _get_mirror_cell(self, row, col):
        """
        Get the coordinates of the mirror cell for 180° rotation.
        
        Args:
            row, col: Original cell coordinates
        
        Returns:
            (mirror_row, mirror_col): Mirror cell coordinates
        """
        mirror_row = self.height - 1 - row
        mirror_col = self.width - 1 - col
        return mirror_row, mirror_col
    
    def set_cell(self, row, col, value):
        """
        Set cell value. If symmetry is enforced, also sets mirror cell.
        
        Args:
            row, col: Cell coordinates
            value: None (empty), '#' (black), or single character
        """
        # Bounds check
        if not (0 <= row < self.height and 0 <= col < self.width):
            raise IndexError(f"Cell ({row},{col}) out of bounds")
        
        # Value validation
        if value is not None and value != self.BLACK_SQUARE:
            if len(str(value)) != 1:
                raise ValueError("Value must be single character")
        
        # Set the cell
        self.grid[row][col] = value
        
        # If symmetry enforced, set mirror cell
        if self.enforce_symmetry:
            mirror_row, mirror_col = self._get_mirror_cell(row, col)
            
            # Only auto-set black squares symmetrically
            # (filled letters are handled by CSP solver)
            if value == self.BLACK_SQUARE:
                self.grid[mirror_row][mirror_col] = self.BLACK_SQUARE
            elif value is None:
                # If clearing a cell, clear its mirror too
                self.grid[mirror_row][mirror_col] = None
    
    def set_black_square(self, row, col):
        """
        Convenience method to set a black square.
        If symmetry enforced, automatically sets mirror black square.
        """
        self.set_cell(row, col, self.BLACK_SQUARE)
    
    def check_symmetry(self):
        """
        Check if current grid has 180° rotational symmetry.
        
        Returns:
            bool: True if symmetric, False otherwise
        
        Note: Only checks black square pattern, not filled letters.
        """
        for row in range(self.height):
            for col in range(self.width):
                mirror_row, mirror_col = self._get_mirror_cell(row, col)
                
                cell = self.grid[row][col]
                mirror = self.grid[mirror_row][mirror_col]
                
                # Check black square symmetry
                cell_is_black = (cell == self.BLACK_SQUARE)
                mirror_is_black = (mirror == self.BLACK_SQUARE)
                
                if cell_is_black != mirror_is_black:
                    return False
        
        return True
    
    def enforce_symmetry_retroactively(self):
        """
        Enforce symmetry on an existing grid by mirroring black squares.
        
        For each black square in the grid, ensures its mirror is also black.
        Useful if you created a grid without symmetry and want to fix it.
        """
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == self.BLACK_SQUARE:
                    mirror_row, mirror_col = self._get_mirror_cell(row, col)
                    self.grid[mirror_row][mirror_col] = self.BLACK_SQUARE

    def generate_pattern(self, method='random', black_percentage=0.17, template=None):
        """
        Generate black square pattern.
        
        Args:
            method: 'random', 'template', or 'algorithmic'
            black_percentage: Target percentage of black squares (for random/algorithmic)
            template: Template data (for template method)
        
        Respects self.enforce_symmetry automatically.
        """
        if method == 'random':
            self._generate_random_pattern(black_percentage)
        elif method == 'template':
            self._generate_from_template(template)
        elif method == 'algorithmic':
            self._generate_algorithmic_pattern(black_percentage)
        else:
            raise ValueError(f"Unknown method: {method}. Use 'random', 'template', or 'algorithmic'")

    def _generate_random_pattern(self, black_percentage):
        """Generate random black square pattern."""
        import random
        
        target_blacks = int(self.width * self.height * black_percentage)
        
        if self.enforce_symmetry:
            # Only iterate through half the grid (symmetry handles the rest)
            half_height = (self.height + 1) // 2
            half_width = (self.width + 1) // 2
            
            placed = 0
            attempts = 0
            max_attempts = self.width * self.height * 10
            
            while placed < target_blacks // 2 and attempts < max_attempts:
                row = random.randint(0, half_height - 1)
                col = random.randint(0, half_width - 1)
                
                # Skip center cell for odd grids
                if self.height % 2 == 1 and self.width % 2 == 1:
                    center_row = self.height // 2
                    center_col = self.width // 2
                    if row == center_row and col == center_col:
                        attempts += 1
                        continue
                
                if not self.is_black(row, col):
                    self.set_black_square(row, col)
                    placed += 1
                
                attempts += 1
        
        else:
            # No symmetry - place anywhere
            placed = 0
            attempts = 0
            max_attempts = self.width * self.height * 10
            
            while placed < target_blacks and attempts < max_attempts:
                row = random.randint(0, self.height - 1)
                col = random.randint(0, self.width - 1)
                
                if not self.is_black(row, col):
                    self.set_black_square(row, col)
                    placed += 1
                
                attempts += 1

    def _generate_from_template(self, template):
        """
        Generate pattern from template.
        
        Args:
            template: 2D list or string representation of pattern
        
        To be implemented - placeholder for now.
        """
        # TODO: Implement template loading
        # Could accept:
        # - 2D list: [[None, '#', None], [None, None, '#'], ...]
        # - String with newlines: "□□■\n□□□\n■□□"
        # - File path: "patterns/nyt_15x15_001.txt"
        raise NotImplementedError("Template pattern generation not yet implemented")

    def _generate_algorithmic_pattern(self, black_percentage):
        """
        Generate pattern using algorithm (more structured than random).
        
        Args:
            black_percentage: Target percentage of black squares
        
        To be implemented - placeholder for now.
        Could use techniques like:
        - Constraint satisfaction to ensure valid word lengths
        - Aesthetic rules (no 2x2 black square blocks, etc.)
        - Theme-aware placement (reserve long slots)
        """
        # TODO: Implement algorithmic generation
        raise NotImplementedError("Algorithmic pattern generation not yet implemented")