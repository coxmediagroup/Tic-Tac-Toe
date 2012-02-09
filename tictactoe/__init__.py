"""A base implementation for a Tic-Tac-Toe game"""


PLAYER_O = 'circle'
PLAYER_X = 'cross'


class MoveNotAvailable(Exception):
    """Thrown when trying to make a move on a tile that was already played on"""
    pass


class InvalidPlayerError(Exception):
    """Thrown when making a move to player other than PLAYER_O or PLAYER_X"""
    pass


class Board(object):
    """The Tic-Tac-Toe board"""

    def __init__(self):
        self.board = [
                [None, None, None],
                [None, None, None],
                [None, None, None],
            ]

        self.size = 3

    def get_winner(self):
        """Returns true if a player has won"""
        # no winner found
        return None

    def get_move_at_position(self, pos):
        """Returns the move at the specified position"""

        if pos[0] >= self.size or pos[1] >= self.size:
            raise IndexError()

        return self.board[pos[0]][pos[1]]

    def add_move(self, pos, player):
        """Adds a move to the board at position `pos` by player `player`"""

        current_move_at_pos = self.get_move_at_position(pos)

        if current_move_at_pos is not None:
            raise MoveNotAvailable()

        if player not in (PLAYER_X, PLAYER_O):
            raise InvalidPlayerError()

        self.board[pos[0]][pos[1]] = player


class AIPlayer(object):
    """An AI Tic-Tac-Toe player

    Guaranteed to always at least stalemate
    """

    def __init__(self, player):
        pass

    def get_next_move(self, board):
        """Returns the position of the next move"""
        pass
