

class PlayException(Exception):
    """You're cheating!"""


class Board(object):
    """Represents a basic tic-tac-toe board"""

    def __init__(self):
        self.li_grid = [[None] * 3 for x in range(3)]

    def play(self, marker, row, col):
        """places marker on the board"""
        cur_val = self.li_grid[row][col]
        if cur_val != None:
            raise PlayException()
        self.li_grid[row][col] = marker


class Player(object):
    """ abstract class that represents a Player"""

    def __init__(self, board, marker, other_marker):
        self.board = board
        self.marker = marker
        self.other_marker = other_marker

    def _available_moves_(self):
        li_moves = []
        for row in range(3):
            for col in range(3):
                if self.board.li_grid[row][col] == None:
                    li_moves.append([row, col])
        return li_moves


class AIPlayer(Player):
    pass
