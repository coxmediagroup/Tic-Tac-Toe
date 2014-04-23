
from django.contrib.auth.models import User

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Board(models.Model):
    """
    Represents a game board.
    """
    rows = models.IntegerField(default=3)
    columns = models.IntegerField(default=3)
    state = models.CharField(max_length=256)


class GameManager(models.Manager):
    pass

class Game(models.Model):
    """
    Represents a game, which is essentially a combination
    of state, a board, and players.
    """
    board = models.ForeignKey('Board',
        verbose_name=_('board'), )
    players = models.ManyToManyField(User,
        verbose_name=_('players'),
        related_name='players')

    turn_counter = models.IntegerField()
    date_started = models.DateTimeField(auto_now_add=True)
    last_play = models.DateTimeField(auto_now=True)

    game_over = models.BooleanField(default=False)
    winner = models.ForeignKey(User, related_name='games_won')

    objects = GameManager()


