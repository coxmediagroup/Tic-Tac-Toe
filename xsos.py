class Grid(object):
    """
    A simple class for playing X's & O's (tic tac toe).
    """
    # marks as constants
    X = 1
    O = 2
    grid = []
    # size of the grid
    size = None
    
    def __init__(self, size=3):
        """
        Constructs a square grid of the given size (3 by default).
        """
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
    
    def _get_rotated_grid(self):
        """
        Returns self.grid rotated 90 degrees so columns become rows.
        
        See http://mail.python.org/pipermail/tutor/2006-November/051039.html
        """
        size = self.size
        return [[self.grid[col][size-row-1] for col in range(size)] for row in range(size)]
    
    def _get_diagonal_rows(self):
        """
        Returns the 2 diagonals 
        """
        size = self.size
        rng = range(size)
        return [[self.grid[x][x] for x in rng], [self.grid[x][size-x-1] for x in rng]]
    
    def _get_all_rows(self):
        """
        Returns the grid with the addition of columns and diagonals as rows.
        """
        return self.grid + self._get_rotated_grid() + self._get_diagonal_rows()
    
    def game_over(self):
        """
        Checks to see if the game is over.
        
        Returns a boolean.
        """
        size = self.size
        
        for r in self._get_all_rows():
            # only check rows that are full
            if 0 not in r and not sum(r)%size:
                    return True
        return False
    
    def play(self):
        """
        Plays the game of tic tac toe
        """
        players = ('X', 'O')
        over = self.game_over()
        rng = range(self.size)
        while not over:
            for p in players:
                print("Player %s is up!" % p)
                print("Current Board:")
                print(self.grid)
                valid_cell = False
                while not valid_cell:
                    print "Please choose an open cell to place your mark"
                    r = -1
                    while r not in rng:
                        i = raw_input("Please select a row (1-%s): " % str(self.size))
                        try:
                            r = int(i) - 1
                        except:
                            print "Please enter a valid choice."
                            continue
                    c = -1
                    while c not in rng:
                        i = raw_input("Please select a column (1-%s): " % str(self.size))
                        try:
                            c = int(i) - 1
                        except:
                            print "Please enter a valid choice."
                            continue
                    valid_cell = not self.grid[r][c]
                self.grid[r][c] = getattr(self, p)
                over = self.game_over()
        print "The game is over."
    