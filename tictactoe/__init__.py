"""
Implementation for the game ``Board`` and ``naught_bot`` that will play the game
"""
from .exceptions import SizeError, DoubleMoveError, NonEmptyCellError, FirstPlayerRequiredError

class Board(object):
    """The board enforces the game rules."""

    NAUGHT = False
    CROSS = True
    EMPTY = None
    __cells = None
    __first_player = None

    @classmethod
    def __empty_board(cls):
        return [cls.EMPTY, ] * 9

    def __init__(self, cells=None, first_player=None):
        """
        :param cells: list of cell states
        :param first_player: set who made the first mark on the board
        """
        self.__first_player = None
        if cells is not None and first_player is None:
            raise FirstPlayerRequiredError("first_player is required when setting cells")
        elif cells is None and first_player:
            first_player = None

        self.__cells = cells if cells is not None else self.__empty_board()
        if len(self.__cells) != 9:
            raise SizeError("Unexpected Board size. Board must have 9 cells.")

    @property
    def cells(self):
        return (cell for cell in self.__cells)

    @staticmethod
    def __coords_to_index(x, y):
        return (x * 3) + y

    def __getitem__(self, item):
        return self.__cells[item]

    def __setitem__(self, key, value):
        if self.__cells[key] is not self.EMPTY:
            raise NonEmptyCellError

        # note who placed the first mark on the board
        if self.__cells.count(self.EMPTY) == 9:
            self.__first_player = value

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
                raise DoubleMoveError

        except DoubleMoveError as exc:
            # we are try/excepting so the assignment to the cells list is
            # rolled back, but we still want the exception to bubble up.
            self.__cells[key] = original_val
            raise exc






def naught_bot(board):
    """Evaluates the board state and decides which cell it wants to mark.
    :param board: A :class:`Board` instance evaluate.
    :returns: index of the cell it intends to mark.
    """
