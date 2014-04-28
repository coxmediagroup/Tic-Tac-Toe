"""Tic-tac-toe AI and win detection.

See __init__.py docstring for more info.

"""

from . import board_model


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


def try_block_opponent(board, ai_piece):
    """Look for imminent wins from the opponent and attempt to block them.

    :param board: The board model
    :param ai_piece: The symbol the AI is playing as; either 'X' or 'O'

    :returns:
        A ``(row, col)`` position the AI should move to block a victory, or
        ``None`` if there are no ways to block a victory on this turn.

    """
    ai_move = None

    for line in board_model.LINES:
        x_cells, o_cells, empty_cells = board_model.organize_cells(line,
                                                                   board)
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

    for line in board_model.LINES:
        x_cells, o_cells, empty_cells = board_model.organize_cells(line,
                                                                   board)
        if len(o_cells) == 2 and len(empty_cells) == 1:
            ai_move = empty_cells[0]
            break

    return ai_move


def try_block_diagonal_traps(board):
    """Return a move that blocks diagonal traps if one is in progress.

    This function assumes it's turn #3 and the AI is playing as O.

    There are two diagonal traps. The first:

        '  0'
        ' X '
        'X  '

    In this situation, O must take either open corner. Otherwise, when X takes
    one of them, he will have two lines available to win.

    The other:

        '  X'
        ' O '
        'X  '

    In this situation, O must **not** take a corner. Otherwise, X will take
    the opposite corner, which will give him two lines available to win.

    :returns:
        A suitable blocking move, or ``None`` if there are no diagonal traps
        to block.

    """
    ai_move = None

    def diagonal_filled(diagonal):
        return all(board[r][c] != ' ' for r, c in diagonal)

    a_diagonal_is_filled = any(diagonal_filled(d) for d in
                               board_model.DIAGONALS)

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

    return ai_move


def get_corner_cell_between_edge_cells(edge_a, edge_b):
    """Get the coordinates of the corner cell between the two edge cells.

    An 'edge cell' is any non-corner cell, and not the center cell.

    E.g.::

        >>> get_corner_cell_between_edge_cells((0, 1), (1, 2))
        (0, 2)
        >>> get_corner_cell_between_edge_cells((1, 0), (2, 1))
        (2, 0)

    """
    # the two edge cells together surround a corner. E.g.
    # 'top center' and 'right center' implies 'top-right
    # corner.' Since all the cells are center cells, the
    # non-1 coordinate from both cells, when combined, will
    # be the appropriate corner. E.g. (0, 1), (1, 2) is the top
    # and right edge, and (0, 2) is the top-right corner
    a_row, a_col = edge_a
    b_row, b_col = edge_b
    if a_row == 2 or b_row == 2:
        corner_row = 2
    else:
        corner_row = 0

    if a_col == 2 or b_col == 2:
        corner_col = 2
    else:
        corner_col = 0

    return corner_row, corner_col


def try_block_corner_trap(board):
    """Return a move that blocks corner traps if one is in progress.

    This function assumes it's turn #3 and the AI is playing as O.

    A corner trap:

        ' X '
        ' OX'
        '   '

    In this situation, if O does not move on (0, 0), (0, 2) or (2, 2), X can
    guarantee a win by marking (0, 2)

    :returns:
        A suitable blocking move, or ``None`` if there's no corner trap in
        progress.

    """
    ai_move = None
    edges = [(0, 1), (1, 2), (2, 1), (1, 0)]

    # range starts at -1 to capture the (edges[-1], edges[0]) pair
    edge_pairs = ((edges[n], edges[n+1]) for n
                  in range(-1, len(edges)-1))

    for (a_row, a_col), (b_row, b_col) in edge_pairs:
        if board[a_row][a_col] == board[b_row][b_col] == 'X':
            ai_move = get_corner_cell_between_edge_cells((a_row, a_col),
                                                         (b_row, b_col))

    return ai_move


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

    # check for special situations and try to assign 'ai_move'
    if turn_num == 1:

        # take the center if open, otherwise take any corner
        if board[1][1] != 'X':
            ai_move = (1, 1)
        else:
            ai_move = (0, 0)

    elif turn_num == 3:

        ai_move = try_block_diagonal_traps(board)

        # a strange condition; player X gave the center to O and didn't set up
        # a diagonal trap; this can still trap the AI.
        if not ai_move and board[1][1] == 'O':
            ai_move = try_block_corner_trap(board)

    # if a special case rule above haven't picked a position...
    if not ai_move:
        winning_move = try_win(board, 'O')
        if winning_move:
            ai_move = winning_move

    if not ai_move:
        blocking_move = try_block_opponent(board, 'O')
        if blocking_move:
            ai_move = blocking_move

    # nothing obvious to do so take any empty cell
    if not ai_move:

        _, _, empty_cells = \
            board_model.organize_cells(board_model.ENTIRE_BOARD, board)

        ai_move = empty_cells[0]

    return 'O', ai_move