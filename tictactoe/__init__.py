"""
Implementation for the game ``Board`` and ``naught_bot`` that will play the game
"""
import itertools
from . import exceptions as ex

NAUGHT = False
CROSS = True
EMPTY = None


class Board(object):
    """The board enforces the game rules."""

    __cells = None
    __first_player = None
    __winner = None

    def __repr__(self):
        substitutions = {
            EMPTY: " ",
            NAUGHT: "o",
            CROSS: "x",
        }

        return (" {0} | {1} | {2} \n"
                "===========\n"
                " {3} | {4} | {5} \n"
                "===========\n"
                " {6} | {7} | {8} \n"
                ).format(*map(lambda v: substitutions[v], self.cells))

    __str__ = __repr__

    @classmethod
    def __empty_board(cls):
        return [EMPTY, ] * 9

    def __init__(self, cells=None, first_player=None):
        """
        :param cells: list of cell states
        :param first_player: sets who made the first mark on the board (required
                             when cells is not None).
        """
        if cells is None:
            # when cells is None, we start with an empty board (and therefore
            # can't have a first player).
            first_player = None
            cells = self.__empty_board()
        elif first_player is None:
            raise ex.FirstPlayerRequiredError("first_player is required when "
                                              "setting cells for initial state")

        self.__first_player = first_player
        self.__cells = cells

        if len(self.__cells) != 9:
            raise ex.SizeError("Unexpected Board size. "
                               "Board must have 9 cells.")

    @property
    def first_player(self):
        return self.__first_player

    @property
    def cells(self):
        return (cell for cell in self.__cells)

    @property
    def rows(self):
        return (indexes for indexes in [(0, 1, 2), (3, 4, 5), (6, 7, 8)])

    @property
    def columns(self):
        return (indexes for indexes in [(0, 3, 6), (1, 4, 7), (2, 5, 8)])

    @property
    def diagonals(self):
        return (indexes for indexes in [(0, 4, 8), (2, 4, 6)])

    @property
    def groupings(self):
        """combines the index generators returned by
        ``rows``, ``columns``, and ``diagonals`` to simplify searching through
        the board for win opportunities."""
        return itertools.chain(self.rows, self.columns, self.diagonals)

    @property
    def winner(self):
        if self.__winner is None:
            for cells in self.groupings:
                group = self[cells]
                if group.count(NAUGHT) == 3:
                    self.__winner = NAUGHT
                    break
                elif group.count(CROSS) == 3:
                    self.__winner = CROSS
                    break
        return self.__winner

    def game_is_over(self):
        return self.winner is not None or self.__cells.count(EMPTY) == 0

    def __getitem__(self, item):

        try:
            # When item is a sequence we'll return a list of the values for
            # the indexes specified.
            return [self.__cells[int(i)] for i in item]
        except TypeError:
            # otherwise ensure we only get a single int argument (not a slice).
            return self.__cells[int(item)]

    def __setitem__(self, key, value):
        if value not in (NAUGHT, CROSS):
            raise ValueError

        if self.__cells[key] is not EMPTY:
            raise ex.NonEmptyCellError(key)

        if self.__first_player is None:
            # Note who placed the first mark on the board
            self.__first_player = value
        elif self.winner is not None:
            # If there's a winner already, raise out before the assignment
            # is made.
            raise ex.GameOver(winner=self.winner)

        original_val = self.__cells[key]

        try:
            self.__cells[key] = value
            crosses = self.__cells.count(CROSS)
            naughts = self.__cells.count(NAUGHT)

            # First player should always be the player to "lead" the mark count
            # (if the counts are equal, the next move belongs to the first
            # player).
            # Neither player should ever have more than a 1 mark lead/gap on
            # the board.
            lead_belongs_to_player_two = (crosses != naughts
                                          and value != self.__first_player)
            gap_too_large = max(crosses, naughts) - min(crosses, naughts) > 1
            if  gap_too_large or lead_belongs_to_player_two:
                raise ex.DoubleMoveError

            if self.game_is_over():
                raise ex.GameOver(winner=self.winner)

        except ex.DoubleMoveError:
            # we are try/excepting so the assignment to the cells list is
            # rolled back, but we still want the exception to bubble up.
            self.__cells[key] = original_val
            raise


def naught_bot(board):
    """Evaluates the board state and decides which cell it wants to mark.
    :param board: A :class:`Board` instance evaluate.
    :returns: index of the cell it intends to mark.
    """
    if board[4] is EMPTY:
        # always take the center if it's open
        return 4

    # Test for naught first since a win is better than a block
    for mark in (NAUGHT, CROSS):
    # Critical cells are those that have 1 empty and 2 of the same mark, they
    # should be addressed first.
        for cells in board.groupings:
            values = board[cells]

            if values.count(EMPTY) == 1 and values.count(mark) == 2:
                return cells[values.index(EMPTY)]

    corners = (0, 2, 6, 8)
    edges = (1, 3, 5, 7)
    # corners are generally better targets than edges
    if board[4] is NAUGHT and list(board[corners]).count(CROSS) > 1:
        return next(idx for (idx, val) in enumerate(board.cells)
                    if idx in edges and val is EMPTY)
    elif board[corners].count(EMPTY) > 0:
        return next(idx for (idx, val) in enumerate(board.cells)
                    if idx in corners and val is EMPTY)
    # if there are no corners free, just pick the first available open cell
    return next(idx for idx, val in enumerate(board.cells) if val is EMPTY)

