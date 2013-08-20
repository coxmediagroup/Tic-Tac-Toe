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

#'Pre-computed' neighborhood map
NEIGHBORS = {0: [1, 3, 4],
    1: [0, 4, 2],
    2: [1, 4, 5],
    3: [0, 4, 6],
    4: [0, 1, 2, 3, 5, 6, 7, 8],
    5: [2, 4, 8],
    6: [3, 4, 7],
    7: [6, 4, 8],
    8: [7, 4, 5]}


def _scoreBoard(board):
    """Interate through the board and bump the score for each empty cell. If
    there's a good reason (winning move, prevent opponent winning more) then
    bump the score again. The objective is the cell with the highest probability
    of winning the game should get the highest score.

    The heuristic is this:
     +1 point if the cell is empty
     +1 point if the cell is a corner
     +1 point if the cell is next to one of our marks
     -1 point if the cell is next to an oppenent's mark
    """
    wp_SCORES = [1] + [0 for x in xrange(0, 8)]
    for x in xrange(0, 9):
        cell = board[x]
        if cell is None:
            wp_SCORES[x] += 1
            #Check the neighbors
            neighbors = NEIGHBORS[x]
            for y in neighbors:
                if board[y] == 'X':
                    wp_SCORES[x] += 1
                if board[y] == 'O':
                    wp_SCORES[x] -= 1
        #unoccupied coners get an extra point
        if cell is None and x in (0, 2, 6, 8):
            wp_SCORES[x] += 1
    #Cleanup any mis-scored cells
    for x in xrange(0, 9):
        if board[x] is not None:
            wp_SCORES[x] = 0
    return wp_SCORES


def winningPlayer(board):
    """Referencing the wikipedia page (http://en.wikipedia.org/wiki/Tic-tac-toe)
    it seems like the best strategy is to take a corner first which prevents
    the opposing player from going down a lot of forks in the game tree.
    """
    #Offense and defense scan
    wp_scores = _scoreBoard(board)

    #Look at the scores, figure out where the hotspot is
    high_score = -1
    target = 1
    for x in xrange(0, 9):
        if wp_scores[x] > high_score:
            high_score = wp_scores[x]
            target = x

    #make a move
    board[target] = 'X'
    return wp_scores
