from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    """
    Represents a match between two players.
    """
    startedOn = models.DateTimeField(auto_now_add=True)
    player1 = models.ForeignKey(User, related_name='player1')
    player2 = models.ForeignKey(User, related_name='player2')

    