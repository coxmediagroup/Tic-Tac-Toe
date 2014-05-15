__author__ = 'marc'
"""
Data for the game - participants
"""

class Game():
    """
    store game participants
    Game is rigged for first player, deep_blue!!!
    opponent is the user-player of this 1-gamer game
    """
    def __init__(self, deep_blue, opponent):
        self.deep_blue = deep_blue
        self.opponent = opponent

