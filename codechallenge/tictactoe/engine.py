
from copy import deepcopy

# Constants
BOARD_ROWS = 3
BOARD_COLS = 3
MARK_CROSS = 'X'
MARK_CIRCLE = 'O'
MARK_EMPTY = None

class Board:
    """ Game Board """

    def __init__(self, cells=None):
        # load
        self.cells = cells

        # create if None
        # NOTE: cells are in cells[ROW][COL] format!
        if self.cells is None:
            self.cells = [ ]
            for r in range(BOARD_ROWS):
                row = [ ]
                for c in range(BOARD_COLS):
                    row.append(MARK_EMPTY)
                self.cells.append(row)

    def in_range(self, col, row):
        """ Check if a cell is in range / cordinates are correct """
        return col < BOARD_COLS and row < BOARD_ROWS

    def is_free(self, col, row):
        """ Checks if a cell on board is free """
        return self.in_range(col=col, row=row) and self.cells[row][col] == MARK_EMPTY

    def mark(self, col, row, mark):
        """ Mark a cell as taken w/ mark """
        # check if free first
        if not self.is_free(col=col, row=row):
            return False

        # mark it
        self.cells[row][col] = mark
        return True

    def cell_class(self, row, col):
        """ returns the cells with values as classes for use in template """
        if not self.in_range(row=row, col=col):
            return MARK_EMPTY
        
        # store cell
        cell = self.cells[row][col]

        # fontawesome class mark
        if cell == MARK_CROSS:
            return 'fa-times'
        elif cell == MARK_CIRCLE:
            return 'fa-circle-o'
        return ''

    @property
    def possible_moves(self):
        """ generate a list of dictionaries w/ all possible moves left
        :return: a list of dict w/ keys (row, col) of possible moves
        """
        moves = [ ]
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.is_free(row=row, col=col):
                    moves.append(dict(row=row, col=col))
        return moves

    def to_dict(self):
        """ Save the session to a dictionary """
        return { 'cells': deepcopy(self.cells) }

    @classmethod
    def from_dict(cls, state):
        """ Load the board state from a dictionary """
        cells = deepcopy(state['cells']) if 'cells' in state else [ ]
        return cls(cells=cells)

class GameEngine:
    """ TicTacToe game engine """
    def __init__(self, board=None, user_mark=MARK_CROSS):
        # construct a game board if None
        self.board = Board() if not board else board
        self.user_mark = user_mark if user_mark else MARK_CROSS

    @property
    def engine_mark(self):
        """ returns the mark used by the engine """
        return MARK_CIRCLE if self.user_mark == MARK_CROSS else MARK_CROSS

    def is_free(self, col, row):
        """ Check if a cell is free
        :return: True if empty / free
        """
        return self.board.is_free(col=col, row=row)

    def mark(self, col, row, mark):
        """ mark a cell as taken by mark
        :return: True if mark was successfully set
        """
        return self.board.mark(col=col, row=row, mark=mark)

    def mark_player(self, col, row):
        """ mark a cell as taken by the user
        :return: True if the mark was successfully set
        """
        return self.mark(col=col, row=row, mark=self.user_mark)

    def mark_engine(self, col, row):
        """ mark a cell as taken by the game engine
        :return: True if the mark was successfully set
        """
        return self.mark(col=col, row=row, mark=self.engine_mark)

    def move_next(self):
        """ calculates the next best move to be made and sets a mark there
        :return: True if the mark was successfully set
        """
        # TODO: actual logic
        # mark the first possible move
        if self.gameover:
            return False
        return self.mark_engine(**self.board.possible_moves[0])

    @property
    def gameover(self):
        """ Checks if the game is over
        :return: True if the game is over / all marks are set
        """
        return not self.board.possible_moves

    def to_dict(self):
        """ Save the game engine state to dictionary """
        return {
            'board': self.board.to_dict(),
            'user_mark': self.user_mark
        }

    @classmethod
    def from_dict(cls, state):
        """ Load the game engine from a dictionary """
        board = Board.from_dict(state['board']) if 'board' in state else Board()
        user_mark = state['user_mark'] if 'user_mark' in state else None
        return cls(board=board, user_mark=user_mark)

