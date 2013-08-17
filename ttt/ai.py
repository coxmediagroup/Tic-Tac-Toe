"""This is a collection of functions that implement various
players for a tic-tac-toe game. The idea here is we can
drop in different player 'types' for a different play
experince.

Nick Loadholtes <nick@ironboundsoftware.com>
"""

import random


def randomPlayer(board):
    """Literally just look for an empty spot and put
    our X in the first one we find."""
    pos = random.randrange(0, 9)
    while(board[pos] is not None):
        pos = random.randrange(0, 9)
    board[pos] = 'X'


def winningPlayer(board):
    pass
