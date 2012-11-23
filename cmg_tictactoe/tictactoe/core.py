import re

EMPTY = u'_'
X = u'x'
O = u'o'


class Grid(list):
    """
    A grid in a game of Tic-tac-toe.

    Unplayed positions are represented by ``_``. Played positions are
    represented by ``x`` or ``o``.
    """
    NUM_POSITIONS = 9
    POSITIONS = tuple(xrange(NUM_POSITIONS))
    WINNING_SEQUENCES = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )
    CENTER = 4
    SIDES = (1, 3, 5, 7)
    CORNERS = (0, 2, 6, 8)
    OPPOSITE_CORNERS = ((0, 8), (2, 6))
    GRID_RE = re.compile('[%s%s%s]{%s}' % (EMPTY, X, O, NUM_POSITIONS))

    # TODO: Remove pop, remove, reverse, and sort.
    # TODO: Limit append, extend, insert to only allow up to NUM_POSITIONS.
    # TODO: When item is being set, validate that it is _, x, or o. Also set
    # the state of the game (in-progress, complete) after an item is set.
    # And render the grid immutable if there is a winning sequence.

    def __init__(self, positions=None):
        if positions is None:
            positions = ''.join([EMPTY for x in self.POSITIONS])
        # TODO: Do some validation to only allow 9 items, no more, no less.
        super(Grid, self).__init__(positions)

    def __unicode__(self):
        return ''.join([x for x in self])

    def positions(self, mark=EMPTY):
        """ Returns a list of all positions matching the given mark. """
        return [p for p in self.POSITIONS if self[p] == mark]

    def is_complete(self):
        """
        Returns True if every position has been played in.

        This behavior will likely be changed to return True when the game has
        been won, which requires a winning sequence, not all positions filled.
        """
        return self.count(X) + self.count(O) == self.NUM_POSITIONS

    def is_turn(self, mark):
        """ Return true if the given mark (X or O) is allowed to play. """
        if self.is_complete():
            return False
        # Again we assume that X went first.
        x_turn = self.count(X) == self.count(O)
        return x_turn if mark == X else not x_turn


class Player(object):
    """ A class that can choose the next turn in a game and never loose. """

    def __init__(self, mark=X, opponent=O, grid=None):
        self.x = mark
        self.o = opponent
        self.grid = grid or Grid()

    def _complete_winning_sequence(self, mark):
        # TODO: If possible, refactor this to be more readable and to fail
        #       faster.
        for position in self.grid.positions():
            for seq in self.grid.WINNING_SEQUENCES:
                if position in seq:
                    if len([x for x in seq if x in self.grid.positions(mark)]) == 2:
                        return position

    def form_winning_sequence(self):
        return self._complete_winning_sequence(self.x)

    def prevent_winning_sequence(self):
        return self._complete_winning_sequence(self.o)

    def _form_fork(self, mark):
        # TODO: Refactor this to be more readable and to fail faster.
        oppo = self.o if mark is self.x else self.x
        for position in self.grid.positions():
            for seq in self.grid.WINNING_SEQUENCES:
                if position in seq:
                    l = [x for x in seq if x != position]
                    if l[0] not in self.grid.positions(oppo) and l[1] not in self.grid.positions(oppo):
                        if l[0] in self.grid.positions(mark) or l[1] in self.grid.positions(mark):
                            for seq2 in self.grid.WINNING_SEQUENCES:
                                if position in seq2 and seq != seq2:
                                    l2 = [x for x in seq2 if x != position]
                                    if l2[0] not in self.grid.positions(oppo) and l2[1] not in self.grid.positions(oppo):
                                        if l2[0] in self.grid.positions(mark) or l2[1] in self.grid.positions(mark):
                                            return position

    def create_fork(self):
        """ Form two non-blocked lines of two. """
        return self._form_fork(self.x)

    def prevent_fork(self):
        """ Prevent opponent from forming two non-blocked lines of two. """
        return self._form_fork(self.o)

    def play_in_center(self):
        """ Play in the center. """
        if self.grid[self.grid.CENTER] == EMPTY:
            return self.grid.CENTER

    def play_in_corner_opposite_opponent(self):
        """ Play in a corner opposite the opponent. """
        opponent_corners = [c for c in self.grid.CORNERS if self.grid[c] == self.o]

        # Build a dictionary with keys for every corner, with the value being
        # the opposite corner.
        d = dict(self.grid.OPPOSITE_CORNERS)
        d.update({v: k for k, v in d.items()})

        # Now return the first available corner opposite the opponent.
        for corner in opponent_corners:
            if d[corner] in self.grid.positions():
                return d[corner]

    def play_in_corner(self):
        """ Play in any open corner. """
        open_corners = [c for c in self.grid.CORNERS if self.grid[c] == EMPTY]
        if open_corners:
            return open_corners.pop()

    def play_on_side(self):
        """ Play on any open side. """
        open_sides = [s for s in self.grid.SIDES if self.grid[s] == EMPTY]
        # We assume by this eighth and final option in the strategy that
        # there is somewhere to play on a side -- if there is not then there
        # is something wrong with one of the strategic options and we need to
        # know about it. Thus, we do not handle any IndexError here.
        return open_sides.pop()

    def next_position(self):
        """
        Returns the next position that should be played.

        The strategy for never losing Tic-tac-toe; choose the first available
        option:

        1. Form a winning sequence.
        2. Prevent the opponent from forming a winning sequence.
        3. Fork. (Create two non-block sequences of two.)
        4. Block opponent's fork.
        5. Play in the center.
        6. Play in the corner opposite the opponent.
        7. Play in a corner.
        8. Play on a side.

        Source: http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
        """
        if self.grid.is_turn(self.x) and self.grid.positions():
            strategic_options = (
                self.form_winning_sequence,
                self.prevent_winning_sequence,
                self.create_fork,
                self.prevent_fork,
                self.play_in_center,
                self.play_in_corner_opposite_opponent,
                self.play_in_corner,
                self.play_on_side,
            )
            for opt in strategic_options:
                position = opt()
                if position is not None:
                    return position

        # There are no open positions or it is not our turn.
        return None

    def play(self):
        """
        Determine the next position to play in and then mark it.

        Returns the position played and the updated grid.
        """
        position = self.next_position()
        if position in self.grid.POSITIONS:
            self.grid[position] = self.x

        return position, self.grid
