import json

from django.db import models
from django.db.models.signals import post_init


DEFAULT_BOARD = '000000000'
COMPUTER_MARK = '1'
PLAYER_MARK = '2'


class Game(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TicTacToe(Game):
    board = models.CharField(max_length=9, default=DEFAULT_BOARD)
    move_count = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return 'Tic-Tac-Toe - {}'.format(self.name)

    def move_player(self, position):
        try:
            isinstance(position, int)
        except:
            print 'OH NOEZ'
        else:
            if int(position) <= len(self.board):
                self.board = list(self.board)
                self.board.pop(position)
                self.board.insert(position, COMPUTER_MARK)
                self.board = ''.join(self.board)
                self.save()
        return

    def move_computer(self):
        return

    def status(self):
        return

    def _is_valid_move(self):
        return


def set_board(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.build()
    instance.save()

#post_init.connect(set_board, TicTacToe)
