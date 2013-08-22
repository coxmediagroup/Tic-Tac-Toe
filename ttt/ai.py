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
NEIGHBORS = {0: [[1, 4], [3, 6]],
    1: [[0, 2], [4, 7]],
    2: [[0, 1], [5, 8], [4, 6]],
    3: [[0, 6], [4, 5]],
    4: [[0, 8], [1, 7], [2, 6], [3, 5]],
    5: [[2, 8], [3, 4]],
    6: [[0, 3], [4, 2], [7, 8]],
    7: [[6, 8], [1, 4]],
    8: [[6, 7], [4, 0], [2, 5]]}


def _scoreBoard(board):
    """Interate through the board and bump the score for each empty cell. If
    there's a good reason (winning move, prevent opponent winning more) then
    bump the score again. The objective is the cell with the highest probability
    of winning the game should get the highest score.

    The heuristic is this:
     +1 point for the top right corner (our preferred starting spot)
     +1 point if the cell is empty
     +1 point if the cell is a corner
     +55 points if we have a win situation
     +50 points to block (we prefer a win so it is higher)
     +5 points if there's a X in the neighborhood
     -3 points if there is a mixture of X and O in the neighborhood

     The last one is intended to prevent "low priority" cells from getting
     the move (especially if there's a strategic move that would get missed).
    """
    wp_SCORES = [1] + [0 for x in xrange(0, 8)]
    for x in xrange(0, 9):
        cell = board[x]
        if cell is None:
            wp_SCORES[x] += 1
            #Check the neighbors
            neighbors = NEIGHBORS[x]
            for n in neighbors:
                if board[n[0]] == board[n[1]] and board[n[0]] == 'X':
                    wp_SCORES[x] += 55
                if board[n[0]] == board[n[1]] and board[n[0]] == 'O':
                    wp_SCORES[x] += 50
                if board[n[0]] == 'X' or board[n[1]] == 'X':
                    wp_SCORES[x] += 5
                if board[n[1]] == 'X' and board[n[0]] == 'O':
                    wp_SCORES[x] -= 3
                if board[n[0]] == 'X' and board[n[1]] == 'O':
                    wp_SCORES[x] -= 3
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
