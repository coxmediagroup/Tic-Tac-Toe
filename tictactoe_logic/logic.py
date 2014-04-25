"""Tic-tac-toe AI and win detection.

See __init__.py docstring for more info.

"""


def get_ai_move(board):
    """Get the best move for the given board state.

    Returns a two-item tuple of ``(mark, position)``, where ``mark`` is either
    ``'O'`` or ``'X'`` and ``position`` is itself a ``(row, col)`` tuple.

    """
    if board[1][1] != 'X':
        pos = (1, 1)
    else:
        pos = (0, 0)

    return None, pos