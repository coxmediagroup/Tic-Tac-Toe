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

        # avoid diagonal trap with X at center

        # define diagonals
        topleft_bottomright = (0, 0), (1, 1), (2, 2)
        topright_bottomleft = (0, 2), (1, 1), (2, 0)

        def diagonal_filled(diagonal):
            return all(board[r][c] != ' ' for r, c in diagonal)

        if diagonal_filled(topleft_bottomright):
            pos = (0, 2)
        else:
            pos = (0, 0)

    return 'O', pos