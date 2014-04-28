"""Provide tools to check the Tic-Tac-Toe game state."""
from . import board_model

# constants used for the GameInfo.state property
VICTORY = 'victory'


class GameInfo:
    """Contains information about the state of the board."""

    def __init__(self, win_cells):
        self.state = VICTORY
        self.winner = 'X'
        self.win_cells = win_cells


def check_board(board):
    """Determine the current state of the game.

    :rtype: GameInfo
    :returns: The current state of the game.

    """
    win_row = None
    for row in board_model.ROWS:
        x_cells, o_cells, empty_cells = board_model.organize_cells(row, board)
        if len(x_cells) == 3:
            win_row = row

    return GameInfo(win_row)