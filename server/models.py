"""NDB model definition and Tic Tac Toe game logic."""

import random

from google.appengine.ext import ndb

from messages import GameMessage


class Squares(object):
    ALL = ('a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3')
    NW, N, NE, W, C, E, SW, S, SE = ALL
    CARDINAL = (N, W, E, S)
    ORDINAL = (NW, NE, SW, SE)
    HORIZONTAL = ((NW, N, NE), (W, C, E), (SW, S, SE))
    VERTICAL = ((NW, W, SW), (N, C, S), (NE, E, SE))
    DIAGONAL = ((NW, C, SE), (NE, C, SW))
    TRIPLETS = HORIZONTAL + VERTICAL + DIAGONAL


class Game(ndb.Model):
    """Game play logic with state saved in Datastore."""

    CHARS = ('X', 'O', None)
    WON, LOST, TIED = 'won', 'lost', 'tied'

    a1 = ndb.StringProperty(choices=CHARS)
    a2 = ndb.StringProperty(choices=CHARS)
    a3 = ndb.StringProperty(choices=CHARS)
    b1 = ndb.StringProperty(choices=CHARS)
    b2 = ndb.StringProperty(choices=CHARS)
    b3 = ndb.StringProperty(choices=CHARS)
    c1 = ndb.StringProperty(choices=CHARS)
    c2 = ndb.StringProperty(choices=CHARS)
    c3 = ndb.StringProperty(choices=CHARS)
    outcome = ndb.StringProperty(choices=(WON, LOST, TIED))

    def values(self, squares=Squares.ALL):
        return [getattr(self, square) for square in squares]

    def reset(self):
        for square in Squares.ALL:
            setattr(self, square, None)
        self.outcome = None

    def is_empty_square(self, square):
        return getattr(self, square) is None

    def has_opposite_corners(self):
        """True iff X (user) occupies both corners in a diagonal."""
        for squares in Squares.DIAGONAL:
            values = self.values(squares)
            if values[0] == 'X' and values[2] == 'X':
                return True
        return False

    def get_winning_square(self):
        """Gets winning square for O (computer), or None if not available."""
        for triplet in Squares.TRIPLETS:
            values = self.values(triplet)
            if values.count('O') == 2 and None in values:
                return triplet[values.index(None)]

    def get_blocking_square(self):
        """Gets square for O that blocks X from winning."""
        for triplet in Squares.TRIPLETS:
            values = self.values(triplet)
            if values.count('X') == 2 and None in values:
                return triplet[values.index(None)]

    def get_center_square(self):
        if self.is_empty_square(Squares.C):
            return Squares.C

    def get_most_disruptive_square(self):
        """Gets the square that will affect two X-influenced rows/columns.

        A square is considered "disruptive" if the occupies the same row or
        column as an X. The "most disruptive" square is the one that occupies
        a row and column, each with an X.

        For example:

            +---+---+---+
            |   |   | X |
            +---+---+---+
            |   | O |   |
            +---+---+---+
            |   | X |   | <--- most disruptive square
            +---+---+---+

        """
        if self.has_opposite_corners():
            squares = Squares.CARDINAL
        else:
            squares = Squares.ORDINAL
        for square in squares:
            for horizontal in Squares.HORIZONTAL:
                for vertical in Squares.VERTICAL:
                    if square in horizontal and square in vertical:
                        if self.values(horizontal + vertical).count('X') == 2:
                            if self.is_empty_square(square):
                                return square
        return self.get_random_square(squares)

    def get_random_square(self, squares=Squares.ALL):
        squares = list(squares)
        random.shuffle(squares)
        for square in squares:
            if self.is_empty_square(square):
                return square

    def get_best_square(self):
        """Gets the most effective square for O (computer)."""
        return (self.get_winning_square() or
                self.get_blocking_square() or
                self.get_center_square() or
                self.get_most_disruptive_square() or
                self.get_random_square())

    def is_won(self, char):
        for triplet in Squares.TRIPLETS:
            if self.values(triplet) == [char] * 3:
                return True
        return False

    def is_tied(self):
        return all(self.values())

    def to_message(self):
        """Game instance to ProtoRPC message."""
        return GameMessage(id=self.key.id(), **self.to_dict())
