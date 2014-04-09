from django.db import models
from django.contrib.auth.models import User
import numpy
from datetime import datetime

class TicTacToeGame(models.Model):
    player = models.CharField(max_length=32, default="anonymous")
    game_time = models.DateTimeField()
    board = models.CharField(max_length=17, default="0,0,0,0,0,0,0,0,0")
    
    def __unicode__(self):
        self.print_board()
        return self.player

    def __init__(self, player='Anonymous'):
        super(TicTacToeGame, self).__init__()
        self.player = player
        self.game_time = datetime.now()
        self.save()
        return None

    def get_board(self):
        vals = [int(v) for v in self.board.split(',')]
        board = [vals[0:3], vals[3:6], vals[6:]]
        return board

    
    def set_board(self, board):
        flat_board = [str(i) for i in sum(board, [])]
        self.board = ','.join(flat_board)
        self.save()

    
    def update_board(self, player, position):
        """
        player: 1==computer; 2==human
        """
        board = self.get_board()
        r, c = position
        board[r-1][c-1] = player
        self.set_board(board)

    def print_board(self):
        bn = numpy.array(self.get_board())
        print bn

