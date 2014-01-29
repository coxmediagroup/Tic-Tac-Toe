class Board(object):
    """The tic-tac-toe game board"""
    
    # Board settings
    ROWS = 3
    COLS = 3
    
    # Game rules
    IN_A_ROW = 3
    
    # Players
    P0 = u'-' # player null (blank spaces)
    P1 = u'X' # player one
    P2 = u'0' # player two
    
    def __init__(self):
        self.sanity_check()
        self.board = self.new_board()
        
    def new_board(self):
        """
        Game board is represented as a string of chars
        
        Empty spots are represented by the value of P0
        
        """
        return self.P0 * self.ROWS * self.COLS
    
    def sanity_check(self):
        """
        Basic sanity tests to make the game settings makes sense
        
        """
        # Test the rows and cols are positive integers
        assert int(self.ROWS) > 0, "ROWS must be an integer greater than 0"
        assert int(self.COLS) > 0, "COLS must be an integer greater than 0"
        
        # Test that the game will have a minimal board size
        assert self.ROWS * self.COLS >= 9, "Too few spaces for a game"
        
        # Test that the width of the character for blanks and player is 1 wide
        assert len(self.P0) == 1, "Blank spaces must be one character wide"
        assert len(self.P1) == 1, "Player 1 must be one character wide"
        assert len(self.P2) == 1, "Player 1 must be one character wide"
        
        # Test that there arent any duplicated players or blank characters
        assert self.P0 not in (self.P1, self.P2), "Blank spaces must be unique"
        assert self.P1 not in (self.P0, self.P2), "Player 1 must be unique"
        assert self.P2 not in (self.P0, self.P1), "Player 2 must be unique"
        
        return True