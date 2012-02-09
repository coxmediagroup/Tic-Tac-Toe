"""A base implementation for a Tic-Tac-Toe game"""


PLAYER_O = 'circle'
PLAYER_X = 'cross'


class Board(object):
    """The Tic-Tac-Toe board"""

    def __init__(self):
        pass

    def has_winner(self):
        """Returns true if a player has won"""
        return False

    def get_winner(self):
        """Returns the winning player if a player has won, otherwise None"""
        return 'cross'

    def add_move(self, pos, player):
        """Adds a move to the board at position `pos` by player `player`"""
        pass


class AIPlayer(object):
    """An AI Tic-Tac-Toe player
    
    Guaranteed to always at least stalemate
    """

    def __init__(self, player):
        pass

    def get_next_move(self, board):
        """Returns the position of the next move"""
        pass

