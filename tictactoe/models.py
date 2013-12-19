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

    @classmethod
    def _flip(cls, position):
        return ''.join((position[6:9], position[3:6], position[0:3]))

    @classmethod
    def _rotate(cls, position):
        return ''.join((position[6::-3], position[7::-3], position[8::-3]))

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
