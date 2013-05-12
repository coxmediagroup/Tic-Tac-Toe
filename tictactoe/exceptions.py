"""Exceptions raised by the game"""


class TicTacToeError(Exception):
    """General Exception for the game."""


class FirstPlayerRequiredError(TicTacToeError):
    """Raised when cells are passed to a new Board, but the first_player is not.
    """


class SizeError(TicTacToeError):
    """Raised when the len of cells loaded into the game board are not 9."""


class MoveError(TicTacToeError):
    """General Exception raised when a move can't be made legally."""


class NonEmptyCellError(MoveError):
    """Raised when a player tries to mark a cell that has already been marked.
    """


class DoubleMoveError(MoveError):
    """Raised when a player tries to mark a cell out of turn."""


class GameOver(TicTacToeError):
    """Raised when the game is over. Caller should share who the winner is."""
    winner = None

    def __init__(self, winner):
        assert winner is not None
        self.winner = winner