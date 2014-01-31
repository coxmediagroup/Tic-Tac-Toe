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
        self.last_move = kwargs.get('last_move', False) # optional

    def __str__(self):
        return self.player

class Board(object):
    """
    The game board
    
    """
    def __init__(self, **kwargs):

        # Board settings
        self.ROWS = kwargs.get('rows', 3)
        self.COLS = kwargs.get('cols', 3)

        # Game rules
        self.IN_A_ROW = kwargs.get('IN_A_ROW', 3)

        # Players
        self.P0 = kwargs.get('P0', '-') # player null (blank spaces)
        self.P1 = kwargs.get('P1', 'X') # player one
        self.P2 = kwargs.get('P2', 'O') # player two

        # Scores
        self.P0_score = kwargs.get('P0_score', 0) # Draw
        self.P1_score = kwargs.get('P1_score', 0) # Player 1
        self.P2_score = kwargs.get('P2_score', 0) # Player 2

        # Put a game board together
        self.sanity_check()
        self.board = self.new_board()

    def new_board(self):
        """
        Game board is represented as a 2 dimensional list of BoardSpaces

        """
        board = []
        counter = 1
        for x in range(self.ROWS):
            board.append([])
            for y in range(self.COLS):
                msg = 'row: {}, col: {}, counter: {}, board_index: {}'
                s = BoardSpace(player=self.P0, board_index=counter)
                board[-1].append(s)
                counter += 1
        return board

    def last_space_index(self):
        return self.board[-1][-1].board_index

    def board_position_by_index(self, board_index):
        """
        Given a 1-based index, return the x, y coordinates on the game board

           1-Base Index

        4x3
           1 | 2 | 3 | 4
          --- --- --- ---
           5 | 6 | 7 | 8
          --- --- --- ---
           9 | 10| 11| 12

        3x4
           1 | 2 | 3
          --- --- ---
           4 | 5 | 6
          --- --- ---
           7 | 8 | 9
          --- --- ---
           10| 11| 12

        3x3
           1 | 2 | 3
          --- --- ---
           4 | 5 | 6
          --- --- ---
           7 | 8 | 9

        """
        
        # Raise exception if not possible
        if board_index < 1 or board_index > (self.ROWS * self.COLS):
            msg = '"{}" is out of range for this board.'.format(board_index)
            raise BoardException(msg)
        
        for x, row in enumerate(self.board):
            for y, space in enumerate(row):
                if space.board_index == board_index:
                    return [x,y]

        msg = '"{}" was not found on this board.'.format(board_index)
        raise BoardException(msg)

    def reset_last_move_flag(self):
        """reset last_move flag for every space on board"""
        for row in self.board:
            for space in row:
                space.last_move = False

    def move_player_to_space(self, this_player, board_index):
        x, y = self.board_position_by_index(board_index)
        # Check to see if the space is already occupied
        if self.board[x][y].player == self.P0:
            # set space to player
            self.board[x][y].player = this_player
            # flag the set space as a last move
            self.reset_last_move_flag()
            self.board[x][y].last_move = True
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
            raise BoardException("Too few spaces for this game")

        # Test that the game does not exceed a reasonable board size [256]
        # if self.ROWS * self.COLS > 256:
        #     raise BoardException("Too many spaces for this game")

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