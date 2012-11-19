import re

EMPTY_MARK = u'_'
X_MARK = u'x'
O_MARK = u'o'


class Grid(object):
    """
    A grid in a game of Tic-tac-toe.

    Unplayed positions are represented by ``_``. Played positions are
    represented by ``x`` or ``o``.
    """

    # TODO: Learn if there is a more graceful way to handle all these args and
    # there common default value.
    def __init__(self, p1=EMPTY_MARK, p2=EMPTY_MARK, p3=EMPTY_MARK,
            p4=EMPTY_MARK, p5=EMPTY_MARK, p6=EMPTY_MARK, p7=EMPTY_MARK,
            p8=EMPTY_MARK, p9=EMPTY_MARK):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.p7 = p7
        self.p8 = p8
        self.p9 = p9

    def __unicode__(self):
        return ''.join([self.p1, self.p2, self.p3, self.p4, self.p5, self.p6,
                       self.p7, self.p8, self.p9])

    def is_filled(self):
        # TODO: Do we need the ``{1}`` limiter? Write tests to find out.
        marks = re.findall(r'[xo]{1}', self.__unicode__())
        return len(marks) == 9

    def is_turn(self, mark):
        """ Return true if the given mark (X or O) is allowed to play. """
        if not self.is_filled():
            # TODO: Do we need the ``{1}`` limiter? Write tests to find out.
            xs = re.findall(r'x{1}', self.__unicode__())
            os = re.findall(r'o{1}', self.__unicode__())
            # Again we assume that X went first.
            x_turn = len(xs) == len(os)
            return x_turn if mark == X_MARK else not x_turn
        return False

    def next_turn(self):
        return X_MARK if self.is_turn(X_MARK) else O_MARK

    def mark_position(self, position, mark):
        # TODO: Add validation here that the mark is either and int 1-9 or a
        # string p1-p9.
        # TODO: Decide if validation that mark is not overwriting previous mark
        # is a necessary and/or good thing.
        position = 'p%s' % position if isinstance(position, int) else position
        setattr(self, position, mark)


class Player(object):
    """ A program that can choose the next turn in a game and never loose. """

    def __init__(self, mark=X_MARK, grid=None):
        self.mark = mark
        self.grid = grid or Grid()

    def get_next_position(self):
        if self.grid.is_turn(self.mark):
            return 1
        return None

    def _mark_position(self, position):
        self.grid.mark_position(position, self.mark)

    def play(self):
        position = self.get_next_position()
        if position:
            self._mark_position(position)
