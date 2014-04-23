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

    def get_random_square(self, squares=Squares.ALL):
        squares = list(squares)
        random.shuffle(squares)
        for square in squares:
            if self.is_empty_square(square):
                return square

    def get_best_square(self):
        return self.get_random_square()

    def is_won(self, char):
        for triplet in Squares.TRIPLETS:
            if self.values(triplet) == [char] * 3:
                return True
        return False

    def is_full(self):
        return all(self.values())

    def to_message(self):
        return GameMessage(id=self.key.id(), **self.to_dict())
