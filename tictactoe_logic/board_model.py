"""Tools for working with the board model.

The board model is a list of three strings which are used to represent a
tic-tac-toe board. Each of the three strings is three characters long, and
each character is either:

- 'X' for a cell marked by the X player
- 'O' for a cell marked by the O player
- ' ' for a blank cell

E.g.::

    ['XOX',
     ' XO',
     'X O']

Represents a tic-tac-toe board where X has won on the top-right to bottom-left
diagonal.

"""


ROWS = [((n, 0), (n, 1), (n, 2)) for n in range(3)]


def organize_cells(cells, board):
    """Get an (X_cells, O_cells, empty_cells) tuple for `cells`.

    :param cells: A sequence of ``(row, col)`` pairs (e.g. from ``LINES``)
    :param board: The board model.

    :returns: A tuple, where each tuple is a sequence of positions.

    E.g.::

        >>> board = [
        ...     'X  ',
        ...     ' X ',
        ...     '   ',
        ... ]
        >>> x_cells, o_cells, empty_cells = organize_cells([(0, 0), (1, 1), (2, 2)], board)
        >>> set(x_cells) == {(0, 0), (1, 1)}
        True
        >>> set(o_cells) == set()
        True
        >>> set(empty_cells) == {(2, 2)}
        True

    """
    x_cells = []
    o_cells = []
    empty_cells = []

    for cell in cells:
        row, col = cell
        cell_value = board[row][col]
        if cell_value == 'X':
            x_cells.append(cell)
        elif cell_value == 'O':
            o_cells.append(cell)
        else:
            empty_cells.append(cell)

    return x_cells, o_cells, empty_cells