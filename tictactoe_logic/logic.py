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


# define all lines that are checked for victory
TOP_LEFT_TO_BOTTOM_RIGHT = (0, 0), (1, 1), (2, 2)
TOP_RIGHT_TO_BOTTOM_LEFT = (0, 2), (1, 1), (2, 0)
ROWS = [((n, 0), (n, 1), (n, 2)) for n in range(0, 2)]
COLUMNS = [((0, n), (1, n), (2, n)) for n in range(0, 2)]
DIAGONALS = [TOP_LEFT_TO_BOTTOM_RIGHT, TOP_RIGHT_TO_BOTTOM_LEFT]
LINES = ROWS + COLUMNS + DIAGONALS


def organize_line(line, board):
    """Get an (X_cells, O_cells, empty_cells) tuple for `line`.

    :param line: A sequence of ``(row, col)`` pairs (e.g. from ``LINES``)
    :param board: The board model.

    :returns: A tuple, where each tuple is a sequence of positions.

    E.g.::

        >>> board = [
        ...     'X  ',
        ...     ' X ',
        ...     '   ',
        ... ]
        >>> x_cells, o_cells, empty_cells = organize_line([(0, 0), (1, 1), (2, 2)], board)
        >>> set(x_cells) == {(0, 0), (1, 1)}
        True
        >>> set(o_cells) == set()
        True
        >>> set(empty_cells) == {2, 2}
        True

    """
    x_cells = []
    o_cells = []
    empty_cells = []

    for cell in line:
        row, col = cell
        cell_value = board[row][col]
        if cell_value == 'X':
            x_cells.append(cell)
        elif cell_value == 'O':
            o_cells.append(cell)
        else:
            empty_cells.append(cell)

    return x_cells, o_cells, empty_cells


# TODO: block properly when AI is playing as X
def try_block_opponent(board, ai_piece):
    """Look for imminent wins from the opponent and attempt to block them.

    :param board: The board model
    :param ai_piece: The symbol the AI is playing as; either 'X' or 'O'

    :returns:
        A ``(row, col)`` position the AI should move to block a victory, or
        ``None`` if there are no ways to block a victory on this turn.

    """
    ai_move = None

    for line in LINES:
        x_cells, o_cells, empty_cells = organize_line(line, board)
        if len(x_cells) == 2 and len(empty_cells) == 1:
            ai_move = empty_cells[0]
            break

    return ai_move


def try_win(board, ai_piece):
    """Look for the ability for the AI to win and take it if available.

    :param board: The board model
    :param ai_piece: The symbol the AI is playing as: either 'X' or 'O'

    :returns:
        A ``(row, col)`` position the AI should move to win, or ``None`` if
        there are no winning moves this turn.

    """
    ai_move = None

    for line in LINES:
        x_cells, o_cells, empty_cells = organize_line(line, board)
        if len(o_cells) == 2 and len(empty_cells) == 1:
            ai_move = empty_cells[0]
            break

    return ai_move


# TODO: add more turns
# TODO: handle AI playing as X
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

    elif turn_num == 3:

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

        # a strange condition; player X gave the center to O and didn't set up
        # a diagonal trap; this can still trap the AI. In this state:
        #
        #   ' X '
        #   ' OX'
        #   '   '
        #
        # the AI must mark (0, 0), (0, 2) or (2, 0); otherwise X can force a
        # win by marking (0, 2) on its next turn
        elif board[1][1] == 'O':
            edges = [(0, 1), (1, 2), (2, 1), (1, 0)]

            # range starts at -1 to capture the (edges[-1], edges[0]) pair
            edge_pairs = ((edges[n], edges[n+1]) for n
                          in range(-1, len(edges)-1))

            for edge_a, edge_b in edge_pairs:
                a_row, a_col = edge_a
                b_row, b_col = edge_b
                if board[a_row][a_col] == board[b_row][b_col] == 'X':

                    # the two edge cells together surround a corner. E.g.
                    # 'top center' and 'right center' implies 'top-right
                    # corner.' Since all the cells are center cells, the
                    # non-1 coordinate from both cells, when combined, will
                    # be the appropriate corner. E.g. (0, 1), (1, 2) is the top
                    # and right edge, and (0, 2) is the top-right corner

                    if a_row == 2 or b_row == 2:
                        corner_row = 2
                    else:
                        corner_row = 0

                    if a_col == 2 or b_col == 2:
                        corner_col = 2
                    else:
                        corner_col = 0

                    ai_move = corner_row, corner_col

    # if a special case rule above haven't picked a position...
    if not ai_move:
        blocking_move = try_block_opponent(board, 'O')
        if blocking_move:
            ai_move = blocking_move

    if not ai_move:
        winning_move = try_win(board, 'O')
        if winning_move:
            ai_move = winning_move

    return 'O', ai_move