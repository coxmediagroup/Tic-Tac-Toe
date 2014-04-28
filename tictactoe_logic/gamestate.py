"""Provide tools to check the Tic-Tac-Toe game state."""
from . import board_model


# constants used for the GameInfo.state property
VICTORY = 'victory'
INCOMPLETE = 'incomplete'
DRAW = 'draw'


class GameInfo:
    """Contains information about the state of the board."""

    def __init__(self, state, winner=None, win_cells=None):
        """Create a new GameInfo.

        :param state:
            The current game state. Either ``VICTORY``, ``INCOMPLETE`` or
            ``DRAW``

        :type  winner: str
        :param winner:
            The player who won; either 'X' or 'O'; or ``None`` if the game
            hasn't been won.

        :type  win_cells: sequence
        :param win_cells:
            The cells that make up the line that the winning player completed;
            or ``None`` if the game hasn't been won.

        """
        self.state = state
        self.winner = winner
        self.win_cells = win_cells


def check_board(board):
    """Determine the current state of the game.

    :rtype: GameInfo
    :returns: The current state of the game.

    """
    win_cells = None
    winner = None
    for line in board_model.LINES:
        x_cells, o_cells, empty_cells = board_model.organize_cells(line, board)
        if len(x_cells) == 3:
            win_cells = line
            winner = 'X'
        elif len(o_cells) == 3:
            win_cells = line
            winner = 'O'

    _, _, empty_cells = board_model.organize_cells(board_model.ENTIRE_BOARD,
                                                   board)
    board_is_full = not empty_cells

    if win_cells:
        return GameInfo(VICTORY, winner, win_cells)
    elif board_is_full:
        return GameInfo(DRAW)
    else:
        return GameInfo(INCOMPLETE)