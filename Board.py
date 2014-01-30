class BoardException(Exception):
    pass

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
    
    # Game rules
    IN_A_ROW = 3
    
    P0_score = 0 # Draw
    P1_score = 0 # Player 1
    P2_score = 0 # Player 2
    
    def __init__(self, **kwargs):
        
        # Board settings
        self.ROWS = kwargs.get('rows', 3)
        self.COLS = kwargs.get('cols', 3)
        
        # Players
        self.P0 = kwargs.get('P0', '-') # player null (blank spaces)
        self.P1 = kwargs.get('P1', 'X') # player one
        self.P2 = kwargs.get('P2', 'O') # player two
        
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
    
    def last_space_index(self):
        return self.board[-1][-1].board_index
    
    def player_to_spot(self, this_player, board_index):
        x, y = board_index / self.ROWS, board_index % self.COLS
        if self.board[x][y].player == self.P0:
            self.board[x][y].player = this_player
            return True
        else:
            return False
            
    def sanity_check(self):
        """
        Basic sanity tests to make the game settings makes sense
        
        """
        # Test the rows and cols are positive integers
        if not int(self.ROWS) > 0:
            raise BoardException("ROWS must be an integer greater than 0")
        if not int(self.COLS) > 0:
            raise BoardException("COLS must be an integer greater than 0")
        
        # Test that the game will have a minimal board size
        if not self.ROWS * self.COLS >= 9:
            raise BoardException("Too few spaces for a game")
        
        # Test that the width of the character for blanks and player is 1 wide
        if not len(self.P0) == 1:
            raise BoardException("Blank spaces must be one character wide")
        if not len(self.P1) == 1:
            raise BoardException("Player 1 must be one character wide")
        if not len(self.P2) == 1:
            raise BoardException("Player 1 must be one character wide")
        
        # Test that there arent any duplicated players or blank characters
        if self.P0 in (self.P1, self.P2):
            raise BoardException("Blank spaces must be unique")
        if self.P1 in (self.P0, self.P2):
            raise BoardException("Player 1 must be unique")
        if self.P2 in (self.P0, self.P1):
            raise BoardException("Player 2 must be unique")
        
        return True
    
    def __str__(self):
        string = u''
        for rows in self.board:
            for col in rows:
                string += col.player
        return string