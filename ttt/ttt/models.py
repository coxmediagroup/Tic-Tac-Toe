from django.db import models
from django.contrib.auth.models import User
import numpy
from datetime import datetime

class TicTacToeGame(models.Model):
    player = models.CharField(max_length=32, default="Anonymous")
    game_time = models.DateTimeField(auto_now_add=True)
    board = models.CharField(max_length=17, default="0,0,0,0,0,0,0,0,0")
    
    def __unicode__(self):
        """Does "PrettyPrint" but then just returns challenger name."""
        self.print_board()
        gt = self.game_time
        return 'Challenger: %s %d-%d-%d %d:%d:%d' % (self.player,
                                                     gt.year,
                                                     gt.month,
                                                     gt.day,
                                                     gt.hour,
                                                     gt.minute,
                                                     gt.second)

    def get_board(self):
        vals = [int(v) for v in self.board.split(',')]
        board = [vals[0:3], vals[3:6], vals[6:]]
        return board

    
    def set_board(self, board):
        """Takes in 2D array representation of board, converts it to 
        the string representation and saves it to the database.
        """
        flat_board = [str(i) for i in sum(board, [])]
        self.board = ','.join(flat_board)
        self.save()

    
    def update_board(self, player, position):
        """Updates the board by marking the provided position with the
        provided player's mark.
        player: 1==computer; 2==human
        """
        board = self.get_board()
        r, c = position
        board[r-1][c-1] = player
        self.set_board(board)


    def print_board(self):
        """A "PrettyPrint" of the board."""
        bn = numpy.array(self.get_board())
        print bn


    def open_cell_count(self):
        """Calculates the number of empty cells and returns it."""
        board = self.get_board()
        return sum([1 if c==0 else 0 for c in sum(board,[])])
