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


