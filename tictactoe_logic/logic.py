"""Tic-tac-toe AI and win detection.

See __init__.py docstring for more info.

"""

# TODO: add win condition detection


def get_turn_num(board):
    """Get the current turn number.

    An empty board is considered to be the 0th turn, and turns count upwards
    from there.

    """

    def taken_cells(row):
        """Count the number of nonempty cells in a row."""

        # all rows should be 3 characters long
        return 3 - row.count(' ')

    return sum(taken_cells(row) for row in board)


# TODO: add more turns
# TODO: handle playing as X
def get_ai_move(board):
    """Get the best move for the given board state.

    Returns a two-item tuple of ``(mark, position)``, where ``mark`` is either
    ``'O'`` or ``'X'`` and ``position`` is itself a ``(row, col)`` tuple.

    """

    turn_num = get_turn_num(board)

    # note: any even numbered turn is the AI playing as X, any odd numbered
    # turn is the AI playing as O

    if turn_num == 1:

        # take the center if open, otherwise take any corner
        if board[1][1] != 'X':
            pos = (1, 1)
        else:
            pos = (0, 0)

    else:  # turn 3

        # detect and avoid diagonal traps
        #
        # define the diagonals
        topleft_bottomright = (0, 0), (1, 1), (2, 2)
        topright_bottomleft = (0, 2), (1, 1), (2, 0)
        diagonals = [topleft_bottomright, topright_bottomleft]

        def diagonal_filled(diagonal):
            return all(board[r][c] != ' ' for r, c in diagonal)

        a_diagonal_is_filled = any(diagonal_filled(d) for d in diagonals)
        if a_diagonal_is_filled:

            # if X is at the center, O must take a corner
            if board[1][1] == 'X':

                # (0, 0) and (0, 2) are on opposite diagonals; since only one
                # diagonal is taken, the other must be clear
                if board[0][0] == ' ':
                    pos = (0, 0)
                else:
                    pos = (0, 2)

            # if O is at the center, O must take an 'edge' (non-corner,
            # non-center)
            else:

                # all edges should be open (since only a diagonal is full
                # right now), so just pick one
                pos = (0, 1)
        else:
            pos = (0, 0)

    return 'O', pos