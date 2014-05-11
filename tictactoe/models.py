from django.db import models

from .board import Board
from .strategy import RandomStrategy


class Game(models.Model):
    '''A Tic-Tac-Toe game'''

    IN_PROGRESS = 0
    X_WINS = Board.MARK_X
    O_WINS = Board.MARK_O

    RANDOM_STRATEGY = 0

    state = models.IntegerField(
        help_text='State of the board', default=0)
    server_player = models.IntegerField(
        help_text='Which player is the server?', default=X_WINS,
        choices=((X_WINS, 'X'), (O_WINS, 'O')))
    winner = models.IntegerField(
        help_text='Winner of the game', default=IN_PROGRESS,
        choices=(
            (IN_PROGRESS, 'In Progress'),
            (X_WINS, 'X Wins'),
            (O_WINS, 'O Wins'),
        ))
    strategy_type = models.IntegerField(
        help_text="Server's strategy", default=RANDOM_STRATEGY,
        choices=(
            (RANDOM_STRATEGY, 'Random Strategy'),
        ))

    @property
    def board(self):
        return Board(state=self.state)

    @board.setter
    def board(self, value):
        self.state = value.state()
        self.winner = value.winner() or self.IN_PROGRESS

    @property
    def strategy(self):
        assert self.strategy_type == self.RANDOM_STRATEGY
        return RandomStrategy()
