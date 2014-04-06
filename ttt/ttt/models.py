from django.db import models
from django.contrib.auth.models import User
import numpy

class TicTacToeGame(models.Model):
    player = models.ForeignKey(User)
    game_time = models.DateTimeField()
    board = models.CharField(max_length=17, default="0,0,0,0,0,0,0,0,0")

    
    def get_board(self):
        vals = [int(v) for v in self.board.split(',')]
        board = [vals[0:3], vals[3:6], vals[6:]]
        return board

    
    def set_board(self, board):
        flat_board = sum(board, [])
        self.board = ','.join(flat_board)
        self.save()

    
    def update_board(self, player, position):
        """
        player: 1==computer; 2==human
        """
        board = self.get_board()
        r, c = position
        board[r][c] = player
        self.set_board(board)

    def print_board(self):
        bn = numpy.array(self.get_board())
        print bn

