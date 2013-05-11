"""
Implementation for the game ``Board`` and ``naught_bot`` that will play the game
"""


class Board(object):
    """The board enforces the game rules.
    """
    NAUGHT = False
    CROSS = True
    EMPTY = None

    __game_state = None

    @classmethod
    def __empty_board(cls):
        return [cls.EMPTY, ] * 9

    def __init__(self, game_state=None):
        """:param game_state: list of cell states"""

        self.__game_state = game_state or self.__empty_board()



def naught_bot(board):
    """Evaluates the board state and decides which cell it wants to mark.
    :param board: A :class:`Board` instance evaluate.
    :returns: index of the cell it intends to mark.
    """
