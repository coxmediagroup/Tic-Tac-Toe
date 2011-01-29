"""
Module for AI opponent.
"""

def move(game):
    """
    Move randomly for now.
    """
    import random
    (x, y) = (random.randrange(0, 3), random.randrange(0, 3))
    return game.move("ai", x, y)
