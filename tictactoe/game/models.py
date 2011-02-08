from django.db import models
from game.fields import TicTacToeBoardField

class Game(models.Model):
    """A tic-tac-toe game."""
    board_state = TicTacToeBoardField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
