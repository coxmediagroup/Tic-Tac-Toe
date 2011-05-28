class Grid(object):
    """
    The grid for playing X's & O's (tic tac toe)
    """
    # marks as constants
    X = 1
    O = 2
    grid = []
    # size of the grid
    size = None
    
    def __init__(self, size=3):
        self.size = size
        self._create_grid()
    
    def _create_grid(self):
        """
        Creates the playing grid from self.size in self.grid.  Will desctruct
        an existing grid.
        
        Returns None.
        """
        grid = []
        size = self.size
        rng = range(size)
        for i in rng:
            row = [0]*size
            grid.append(row)
        self.grid = grid
    
    def _rotate_grid(self):
        """
        Rotates self.grid 90 degrees so columns become rows
        
        See http://mail.python.org/pipermail/tutor/2006-November/051039.html
        """
        size = self.size
        return [[self.grid[col][size - row - 1] for col in range(size)] for row in range(size)]
    
    def game_over(self):
        """
        Checks to see if the game is over.
        
        Returns a boolean.
        """
        # check rows
        for r in self.grid:
            # only check rows that are full
            if 0 not in r:
                if not sum(r)%self.size:
                    return True
        # check cols
        for r in self._rotate_grid():
            # only check rows that are full
            if 0 not in r:
                if not sum(r)%self.size:
                    return True
        # check diags
        return False
    