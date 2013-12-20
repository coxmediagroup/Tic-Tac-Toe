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
    state = models.CharField(max_length=9, default='         ')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)
        get_latest_by = 'timestamp'

    SYMMETRY = ('', 'r', 'rr', 'rrr', 'f', 'fr', 'frr', 'frrr')

    @classmethod
    def _flip(cls, position):
        return ''.join((position[6:9], position[3:6], position[0:3]))

    @classmethod
    def _rotate(cls, position):
        return ''.join((position[6::-3], position[7::-3], position[8::-3]))

    @classmethod
    def expand_symmetry(cls, position):
        op_methods = {'f': cls._flip,
                      'r': cls._rotate}

        results = {}
        for operations in cls.SYMMETRY:
            pos = position
            for op in operations:
                pos = op_methods[op](pos)
            results.setdefault(pos, operations)

        return results

    @classmethod
    def _play(cls, position, move):
        return ''.join(move[2] if i == 3 * move[0] + move[1] else c
                       for i, c in enumerate(position))

    @classmethod
    def _is_won(cls, position):
        for S in (position[0:3], position[3:6], position[6:9],
                  position[0::3], position[1::3], position[2::3],
                  position[0::4], position[2:8:2]):
            pieces = set(S)
            if len(pieces) == 1 and pieces != set(' '):
                return True
        return False

    def player(self):
        return 'ox'[self.state.count(' ') % 2]

    def new(self, move):
        if not self.is_legal(move):
            raise Exception("Illegal move.")
        return Position.objects.create(
            game=self.game,
            state=self._play(self.state, (move[0], move[1], self.player()))
        )

    def is_legal(self, move):
        return self.state[3 * move[0] + move[1]] == ' '

    def is_won(self):
        return self._is_won(self.state)


class NextMoveManager(models.Manager):
    @classmethod
    def _flip(self, move):
        return (2 - move[0], move[1])

    @classmethod
    def _rotate(self, move):
        return (move[1], 2 - move[0])

    def lookup(self, state):
        symmetric_states = Position.expand_symmetry(state)
        stored = self.get_query_set().filter(
            state__in=symmetric_states.keys()
        ).get()

        symmetric_states = Position.expand_symmetry(stored.state)
        operations = symmetric_states[state]
        move = (stored.row, stored.column)

        for x in xrange(operations.count('f')):
            move = self._flip(move)
        for x in xrange(operations.count('r')):
            move = self._rotate(move)

        return move


class NextMove(models.Model):
    state = models.CharField(max_length=9)
    row = models.SmallIntegerField()
    column = models.SmallIntegerField()

    objects = NextMoveManager()
