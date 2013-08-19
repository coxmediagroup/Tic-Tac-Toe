"""This is a collection of functions that implement various
players for a tic-tac-toe game. The idea here is we can
drop in different player 'types' for a different play
experince.

Nick Loadholtes <nick@ironboundsoftware.com>
"""

import random

wp_SCORES = [3, 1, 1, 1, 1, 1, 1, 1, 1] #Seeded so we go for the first corner


def randomPlayer(board):
    """Literally just look for an empty spot and put
    our X in the first one we find."""
    pos = random.randrange(0, 9)
    while(board[pos] is not None):
        pos = random.randrange(0, 9)
    board[pos] = 'X'


def winningPlayer(board):
    """Referencing the wikipedia page (http://en.wikipedia.org/wiki/Tic-tac-toe)
    it seems like the best strategy is to take a corner first which prevents
    the opposing player from going down a lot of forks in the game tree.
    """
    #Offense and defense scan
    

    #Look at the scores, figure out where the hotspot is
    high_score = -1
    target = 1
    for x in wp_SCORES:
        if wp_SCORES[x] > high_score:
            high_score = wp_SCORES[x]
            target = x

    #make a move
    board[target] = 'X'
