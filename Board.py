class BoardSpace(object):
    """
    Attributes for a space in a game board
    
    1) player
    2) index value within game board
    3) if this space is part of a winning move
    
    """
    
    def __init__(self, **kwargs):
        self.player = kwargs['player'] # required
        self.board_index = int(kwargs['board_index']) # required
        self.winner = kwargs.get('winner', False) # optional
        
    def __str__(self):
        return self.player

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
    P2 = u'O' # player two
    
    def __init__(self):
        self.sanity_check()
        self.board = self.new_board()
        
    def new_board(self):
        """
        Game board is represented as a 2 dimensional list of BoardSpaces
        
        """
        board = []
        counter = 0
        for x in range(self.ROWS):
            board.append([])
            for y in range(self.COLS):
                s = BoardSpace(player=self.P0, board_index=counter)
                board[-1].append(s)
                counter += 1
        return board
    
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