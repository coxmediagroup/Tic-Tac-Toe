"""
Manage the computer AI for the game.
"""
from itertools import chain
import random

def perform_move(game):
    """
    Analyze the game board and perform the best move.

    Result will not be saved.  That is the responsibility of the caller.
    """
    bs = game.board_state

    # Count how many plays have been made so far: the first and second are
    # special cases.
    number_of_plays = len([cell for cell in chain.from_iterable(bs) if cell is not None])

    # Always take the center square if this is the first move of the game.
    if number_of_plays == 0:
        bs[1][1] = 'X'
        return

    # If this is the second move, try for the center square.  If that is taken,
    # choose any corner.
    if number_of_plays == 1:
        if bs[1][1] is None:
            bs[1][1] = 'X'
        else:
            row = random.choice([0, 2])
            col = random.choice([0, 2])
            bs[row][col] = 'X'
        return

    weighted_moves = generate_weight_table(game)
    selected_row, selected_col = select_move(weighted_moves)
    bs[selected_row][selected_col] = 'X'


def get_number_board(game):
    """
    Converts O's to -1, X's to 1 and None to 0 for all squares on the game
    board for easier calculations.
    """
    bs = game.board_state
    number_board   = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

    for row in xrange(0, 3):
        for col in xrange(0, 3):
            if bs[row][col] == 'X':
                number_board[row][col] = 1
            elif bs[row][col] == 'O':
                number_board[row][col] = -1

    return number_board


def generate_weight_table(game):
    """
    Returns a 2-dimensional array of board squares each ranked such that a
    higher value represents a better move.

    A winning move will always take highest precedence followed by a blocking
    move.
    """
    bs = game.board_state
    number_board = get_number_board(game)
    weighted_moves = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

    for row in xrange(0, 3):
        for col in xrange(0, 3):
            if bs[row][col] is not None:  # Occupied spaces are off limits
                weighted_moves[row][col] = -100
            else:  # Possible play
                ### Create score for row
                row_score = sum(number_board[row])
                if row_score == 2:
                    # This is a winning move, be sure to take it.
                    weighted_moves[row][col] = 100
                elif row_score == -2:
                    # This is a block, it is only less preferable to a win.
                    weighted_moves[row][col] = 50

                ### Create score for column
                col_score = number_board[0][col] + number_board[1][col] \
                          + number_board[2][col]
                if col_score == 2:
                    # This is a winning move, be sure to take it.
                    weighted_moves[row][col] = 100
                elif col_score == -2:
                    # This is a block, it is only less preferable to a win.
                    weighted_moves[row][col] = 50

                ### Create score for diagonal (if corner or middle)
                diag_score = 0
                diag_score1 = number_board[0][0] + number_board[2][2] \
                            + number_board[1][1]
                diag_score2 = number_board[0][2] + number_board[2][0] \
                            + number_board[1][1]
                if row == 1 and col == 1:
                    # This is the middle cell.  We need to consider both
                    # diagonals.
                    if diag_score1 == 2 or diag_score2 == 2:
                        # This is a winning move, be sure to take it.
                        weighted_moves[row][col] = 100
                    elif diag_score1 == -2 or diag_score2 == -2:
                        # This is a block, it is only less preferable to a win.
                        weighted_moves[row][col] = 50
                    diag_score = diag_score1 + diag_score2
                elif row == col:
                    # This cell is on the upper-left to lower-right diagonal.
                    # Just need to consider diag_score1
                    if diag_score1 == 2:
                        # This is a winning move, be sure to take it.
                        weighted_moves[row][col] = 100
                    elif diag_score1 == -2:
                        # This is a block, it is only less preferable to a win.
                        weighted_moves[row][col] = 50
                    diag_score = diag_score1
                elif row + col == 2:
                    # This cell is on the lower-left to upper-right diagonal.
                    # Just need to consider diag_score2
                    if diag_score2 == 2:
                        # This is a winning move, be sure to take it.
                        weighted_moves[row][col] = 100
                    elif diag_score2 == -2:
                        # This is a block, it is only less preferable to a win.
                        weighted_moves[row][col] = 50
                    diag_score = diag_score2

                ### Add the scores together to get total weight
                weighted_moves[row][col] += row_score + col_score + diag_score

    return weighted_moves


def select_move(weight_table):
    """
    Given a 2-dimensional array of board squares individually weighted with
    larger values being better moves, select a move.

    Returns a (row, column) tuple.
    """
    # Consult the weight_table table to pick the best move.  Always pick the
    # cell with the largest number.  If there are multiples with this number,
    # randomly choose one.
    possible_moves = []
    max_num = max(chain.from_iterable(weight_table))

    for row in xrange(0, 3):
        for col in xrange(0, 3):
            if weight_table[row][col] == max_num:
                possible_moves.append((row, col))

    return random.choice(possible_moves)
