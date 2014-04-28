"""Provide tools to check the Tic-Tac-Toe game state."""
from . import board_model

# constants used for the GameInfo.state property
VICTORY = 'victory'
INCOMPLETE = 'incomplete'


class GameInfo:
    """Contains information about the state of the board."""

    @classmethod
    def victory(cls, winner, win_cells):
        return cls(VICTORY, winner, win_cells)

    @classmethod
    def incomplete(cls):
        return cls(INCOMPLETE, None, None)

    def __init__(self, state, winner, win_cells):
        """Create a new GameInfo.

        :param state:
            The current game state. Either ``VICTORY`` or ``INCOMPLETE``

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

    if win_cells:
        return GameInfo.victory(winner, win_cells)
    else:
        return GameInfo.incomplete()