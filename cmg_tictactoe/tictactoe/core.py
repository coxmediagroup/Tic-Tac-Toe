import re


EMPTY = u'_'
X = u'x'
O = u'o'
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
GRID_RE = re.compile('[_%s%s]{%s}' % (X, O, NUM_POSITIONS))


class Grid(list):
    """
    A grid in a game of Tic-tac-toe.

    Unplayed positions are represented by ``_``. Played positions are
    represented by ``x`` or ``o``.
    """

    # TODO: Remove pop, remove, reverse, and sort.
    # TODO: Limit append, extend, insert to only allow up to NUM_POSITIONS.
    # TODO: Render immutable if there is a winning sequence.

    def __init__(self, vals=''.join([EMPTY for x in POSITIONS])):
        # TODO: Do some validation to only allow 9 items, no more, no less.
        super(Grid, self).__init__(vals)

    def __unicode__(self):
        return ''.join([x for x in self])

    def positions(self, mark=EMPTY):
        """ Returns a list of all positions matching the given mark. """
        positions = []
        for position in POSITIONS:
            if self[position] == mark:
                positions.append(position)

        return positions

    def is_complete(self):
        """ Returns True if every position has been played in. """
        return self.count(X) + self.count(O) == NUM_POSITIONS

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
        self.mark = mark
        self.opponent = opponent
        self.grid = grid or Grid()

    def next_position(self):
        """
        The strategy for never losing Tic-tac-toe; choose the first available
        option.

        1. Form a winning sequence.
        2. Prevent the opponent from forming a winning sequence.
        3. Fork?
        4. Block opponent's fork?
        5. Play in the center.
        6. Play in the corner opposite the opponent.
        7. Play in a corner.
        8. Play on a side.
        """
        # TODO: Replace X and O with self.mark and self.opponent, respectively.

        if self.grid.is_turn(self.mark) and self.grid.positions():
            # TODO: Abstract options 1 and 2 into a method. All the same code
            # except the mark.
            # 1. Form a winning sequence.
            for position in self.grid.positions():
                for seq in WINNING_SEQUENCES:
                    if position in seq:
                        l = [x for x in seq if x != position]
                        if l[0] in self.grid.positions(X) and l[1] in self.grid.positions(X):
                            return position

            # 2. Prevent the opponent from forming a winning sequence.
            for position in self.grid.positions():
                for seq in WINNING_SEQUENCES:
                    if position in seq:
                        l = [x for x in seq if x != position]
                        if l[0] in self.grid.positions(O) and l[1] in self.grid.positions(O):
                            return position

            # TODO: Abstract options 3 and 4 into a method. All the same code
            # except the mark.
            # 3. Fork.
            for position in self.grid.positions():
                for seq in WINNING_SEQUENCES:
                    if position in seq:
                        l = [x for x in seq if x != position]
                        if l[0] not in self.grid.positions(O) and l[1] not in self.grid.positions(O):
                            if l[0] in self.grid.positions(X) or l[1] in self.grid.positions(X):
                                for seq2 in WINNING_SEQUENCES:
                                    if position in seq2 and seq != seq2:
                                        l2 = [x for x in seq2 if x != position]
                                        if l2[0] not in self.grid.positions(O) and l2[1] not in self.grid.positions(O):
                                            if l2[0] in self.grid.positions(X) or l2[1] in self.grid.positions(X):
                                                return position

            # 4. Block the opponent's fork.
            for position in self.grid.positions():
                for seq in WINNING_SEQUENCES:
                    if position in seq:
                        l = [x for x in seq if x != position]
                        if l[0] not in self.grid.positions(X) and l[1] not in self.grid.positions(X):
                            if l[0] in self.grid.positions(O) or l[1] in self.grid.positions(O):
                                for seq2 in WINNING_SEQUENCES:
                                    if position in seq2 and seq != seq2:
                                        l2 = [x for x in seq2 if x != position]
                                        if l2[0] not in self.grid.positions(X) and l2[1] not in self.grid.positions(X):
                                            if l2[0] in self.grid.positions(O) or l2[1] in self.grid.positions(O):
                                                return position

            # 5. Play in the center.
            if self.grid[CENTER] == EMPTY:
                return CENTER

            # 6. Play in a corner opposite the opponent.
            opponent_corners = []
            for corner in CORNERS:
                if self.grid[corner] == self.opponent:
                    opponent_corners.append(corner)

            for corner in opponent_corners:
                d = dict(OPPOSITE_CORNERS)
                d.update({v: k for k, v in d.items()})
                if corner in d:
                    return d[corner]

            # 7. Play in a corner.
            open_corners = []
            for corner in CORNERS:
                if self.grid[corner] == EMPTY:
                    open_corners.append(corner)
            if open_corners:
                return open_corners.pop()

            # 8. Finally, play on a side.
            open_sides = []
            for side in SIDES:
                if self.grid[side] == EMPTY:
                    open_sides.append(side)
            return open_sides.pop()

        # There are no open positions or it is not our turn.
        return None

    def play(self):
        """
        Determine the next position to play in and then mark it.

        Returns the position played and the updated grid.
        """
        position = self.next_position()
        if position in POSITIONS:
            self.grid[position] = self.mark

        return position, self.grid
