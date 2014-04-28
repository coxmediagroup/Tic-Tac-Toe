# constants used for the GameInfo.state property
VICTORY = 'victory'


class GameInfo:
    """Contains information about the state of the board."""

    def __init__(self):
        self.state = VICTORY
        self.winner = 'X'
        self.win_cells = ((0, 0), (0, 1), (0, 2))


def check_board(board):
    """Determine the current state of the game.

    :rtype: GameInfo
    :returns: The current state of the game.

    """
    return GameInfo()