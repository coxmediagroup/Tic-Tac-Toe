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


# define some board shortcuts
TOPLEFT_BOTTOMRIGHT = (0, 0), (1, 1), (2, 2)
TOPRIGHT_BOTTOMLEFT = (0, 2), (1, 1), (2, 0)
DIAGONALS = [TOPLEFT_BOTTOMRIGHT, TOPRIGHT_BOTTOMLEFT]


# TODO: add more turns
# TODO: handle playing as X
def get_ai_move(board):
    """Get the best move for the given board state.

    Returns a two-item tuple of ``(mark, position)``, where ``mark`` is either
    ``'O'`` or ``'X'`` and ``position`` is itself a ``(row, col)`` tuple.

    """

    # for identifying special situations, figure out the number of this turn
    turn_num = get_turn_num(board)

    # note: any even numbered turn is the AI playing as X, any odd numbered
    # turn is the AI playing as O

    ai_move = None  # holds the cell that AI will decide to mark

    # check for special situations and try to assign 'pos'

    if turn_num == 1:

        # take the center if open, otherwise take any corner
        if board[1][1] != 'X':
            ai_move = (1, 1)
        else:
            ai_move = (0, 0)

    elif turn_num == 3:  # turn 3

        # detect and avoid diagonal traps
        def diagonal_filled(diagonal):
            return all(board[r][c] != ' ' for r, c in diagonal)

        a_diagonal_is_filled = any(diagonal_filled(d) for d in DIAGONALS)
        if a_diagonal_is_filled:

            # if X is at the center, O must take a corner
            if board[1][1] == 'X':

                # (0, 0) and (0, 2) are on opposite diagonals; since only one
                # diagonal is taken, the other must be clear
                if board[0][0] == ' ':
                    ai_move = (0, 0)
                else:
                    ai_move = (0, 2)

            # if O is at the center, O must take an 'edge' (non-corner,
            # non-center)
            else:

                # all edges should be open (since only a diagonal is full
                # right now), so just pick one
                ai_move = (0, 1)

    # if a special case rule above haven't picked a position...
    if not ai_move:

        # look for chances to block
        columns = [((0, n), (1, n), (2, n)) for n in range(0, 2)]

        lines = DIAGONALS + columns
        for line in lines:
            empty_cells = 0
            empty_cell = None
            x_cells = 0

            for row, col in line:
                if board[row][col] == 'X':
                    x_cells += 1
                elif board[row][col] == ' ':
                    empty_cell = row, col
                    empty_cells += 1

            if x_cells == 2 and empty_cells == 1:
                ai_move = empty_cell

    return 'O', ai_move