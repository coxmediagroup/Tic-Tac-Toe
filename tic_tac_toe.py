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