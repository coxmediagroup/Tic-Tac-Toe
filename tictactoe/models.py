from django.core.urlresolvers import reverse
from django.db import models

from itertools import chain


class Game(models.Model):
    user = models.ForeignKey('auth.User')
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})


class Position(models.Model):
    game = models.ForeignKey(Game, related_name='positions')
    state = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)
        get_latest_by = 'timestamp'

    BITS = {
        'a': 0b111000000,
        'b': 0b000111000,
        'c': 0b000000111,
        '1': 0b100100100,
        '2': 0b010010010,
        '3': 0b001001001,
    }

    DIAGONALS = {
        'up': 0b001010100,
        'down': 0b100010001,
    }

    @property
    def parity(self):
        return bin(self.state).count('1') % 2

    def parse(self, play):
        return self.BITS[play[0]] & self.BITS[play[1]]

    def is_legal(self, play):
        try:
            placement = self.parse(play)
        except (KeyError, IndexError) as e:
            return False

        return not (self.state & (placement | placement << 9))

    def make_move(self, play):
        if not self.is_legal(play):
            raise Exception("Illegal move.")
        placement = self.parse(play) << (9 * self.parity)
        return Position.objects.create(game=self.game,
                                       state=placement | self.state)

    def is_won(self):
        return any(
            (self.state & mask == mask) or ((self.state >> 9) & mask == mask)
            for mask in chain(self.BITS.itervalues(),
                              self.DIAGONALS.itervalues())
        )

    @property
    def array(self):
        x = self.state & 0b111111111
        o = self.state >> 9

        array = []
        for r in reversed(xrange(3)):
            row = []
            for c in reversed(xrange(3)):
                spot = 1 << (3*r + c)
                if spot & x:
                    row.append('X')
                elif spot & o:
                    row.append('O')
                else:
                    row.append(' ')
            array.append(row)

        return array
