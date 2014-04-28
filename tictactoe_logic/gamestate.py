"""Provide tools to check the Tic-Tac-Toe game state."""
from . import board_model

# constants used for the GameInfo.state property
VICTORY = 'victory'


class GameInfo:
    """Contains information about the state of the board."""

    def __init__(self, winner, win_cells):
        """Create a new GameInfo.

        :type  winner: str
        :param winner: The player who won; either 'X' or 'O'

        :type  win_cells: sequence
        :param win_cells:
            The cells that make up the line that the winning player completed

        """
        self.state = VICTORY
        self.winner = winner
        self.win_cells = win_cells


def check_board(board):
    """Determine the current state of the game.

    :rtype: GameInfo
    :returns: The current state of the game.

    """
    win_row = None
    winner = None
    for row in board_model.ROWS:
        x_cells, o_cells, empty_cells = board_model.organize_cells(row, board)
        if len(x_cells) == 3:
            win_row = row
            winner = 'X'
        elif len(o_cells) == 3:
            win_row = row
            winner = 'O'

    return GameInfo(winner, win_row)