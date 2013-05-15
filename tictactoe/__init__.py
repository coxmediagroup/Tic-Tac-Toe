"""
Implementation for the game ``Board`` and ``naught_bot`` that will play the game
"""
import itertools
from . import exceptions as ex


class Board(object):
    """The board enforces the game rules."""

    NAUGHT = False
    CROSS = True
    EMPTY = None
    __cells = None
    __first_player = None
    __winner = None

    def __repr__(self):
        substitutions = {
            self.EMPTY: " ",
            self.NAUGHT: "o",
            self.CROSS: "x",
        }

        return (" {0} | {1} | {2} \n"
                "===========\n"
                " {3} | {4} | {5} \n"
                "===========\n"
                " {6} | {7} | {8} \n"
        ).format(*map(lambda v: substitutions[v], self.cells))

    @classmethod
    def __empty_board(cls):
        return [cls.EMPTY, ] * 9

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
            raise ex.FirstPlayerRequiredError("first_player is required when setting cells")

        self.__first_player = first_player
        self.__cells = cells

        if len(self.__cells) != 9:
            raise ex.SizeError("Unexpected Board size. Board must have 9 cells.")

    @property
    def first_player(self):
        return self.__first_player

    @property
    def cells(self):
        return (cell for cell in self.__cells)

    @property
    def rows(self):
        for row in ((0, 1, 2), (3, 4, 5), (6, 7, 8)):
            yield [self.__cells[i] for i in row]

    @property
    def columns(self):
        for column in ((0, 3, 6), (1, 4, 7), (2, 5, 8)):
            yield [self.__cells[i] for i in column]

    @property
    def diagonals(self):
        for diagonal in ((0, 4, 8), (2, 4, 6)):
            yield [self.__cells[i] for i in diagonal]

    @property
    def groupings(self):
        return itertools.chain(self.rows, self.columns, self.diagonals)

    @property
    def winner(self):
        if self.__winner is None:
            for group in self.groupings:
                if group.count(self.NAUGHT) == 3:
                    self.__winner = self.NAUGHT
                    break
                elif group.count(self.CROSS) == 3:
                    self.__winner = self.CROSS
                    break
        return self.__winner

    def __getitem__(self, item):
        # ensure we only get a single int argument (not a slice).
        return self.__cells[int(item)]

    def __setitem__(self, key, value):
        if value not in (self.NAUGHT, self.CROSS):
            raise ValueError

        if self.__cells[key] is not self.EMPTY:
            raise ex.NonEmptyCellError

        if self.__first_player is None:
            # note who placed the first mark on the board
            self.__first_player = value
        elif self.winner is not None:
            # if there's a winner already, raise out before the assignment is made
            raise ex.GameOver(winner=self.winner)

        original_val = self.__cells[key]

        try:
            self.__cells[key] = value
            crosses = self.__cells.count(self.CROSS)
            naughts = self.__cells.count(self.NAUGHT)

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

            if self.winner is not None:
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
    if list(board.cells).count(board.EMPTY) == 9:
        # this is the opening move
        return 4  # take the center cell
