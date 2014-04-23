from google.appengine.ext import ndb


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

    def reset(self):
        pass

    def is_empty_square(self, square):
        pass

    def get_best_square(self):
        pass

    def is_won(self, char):
        pass

    def is_full(self):
        pass

    def to_message(self):
        pass
