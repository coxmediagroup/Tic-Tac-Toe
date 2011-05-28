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
        rng = range(0,size)
        for i in rng:
            row = [0]*size
            grid.append(row)
        self.grid = grid
    
    def check_game(self):
        """
        Checks to see if the game is over.
        
        Returns a boolean.
        """
        return False
    