from django.db import models

class Game(models.Model):
    """
    Represents a match between two players.
    """
    startedOn = models.DateTimeField(auto_now_add=True)
