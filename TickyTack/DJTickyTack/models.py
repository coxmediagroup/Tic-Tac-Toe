from django.db import models as m
from django.contrib.auth.models import User

class Game(m.Model):
    """
    Represents a match between two players.
    """
    startedOn = m.DateTimeField(auto_now_add=True)
    player1 = m.ForeignKey(User, related_name='player1')
    player2 = m.ForeignKey(User, related_name='player2')
    nextPlayer = m.IntegerField(default=1, choices=((1, 'player1'), (2, 'player2')))

    @property
    def toPlay(self):
        return self.player1 if self.nextPlayer == 1 else self.player2

    