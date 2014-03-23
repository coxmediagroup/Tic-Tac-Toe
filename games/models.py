import json

from django.db import models


DEFAULT_BOARD = '000000000'
EMPTY_MARK = '0'
COMPUTER_MARK = '1'
PLAYER_MARK = '2'
SIZE = 3

class Game(models.Model):
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TicTacToe(Game):
    board = models.CharField(max_length=SIZE, default=DEFAULT_BOARD)
    move_count = models.PositiveIntegerField(null=True, blank=True)

    class Meta(Game.Meta):
        verbose_name = 'Tic Tac Toe'

    def __unicode__(self):
        return '{}'.format(self.__class__.__name__)

    def move_player(self, position):

        if int(position) <= len(self.board) and self._is_valid_move(position):
            self.board = list(self.board)
            self.board.pop(position)
            self.board.insert(position, PLAYER_MARK)
            self.board = ''.join(self.board)
            self.save()

            # Check if the game is complete.
            if self._is_complete():
                print "GAME OVER"
        else:
            print 'OH NOEZ NOT VALID MOVE'
        return

    def move_computer(self):
        return

    def _is_complete(self):
        """Collect all the winning paths and check if game is won or stalemate."""
        winners = []
        board = [list(self.board[x:x+SIZE]) for x in range(0, len(self.board), SIZE)]
       
        # Find all horizontal winning paths.
        for row in board:
            winners.append(row)
       
        # Find all vertical winning paths.
        for x in range(0, SIZE):
            cols = []
            for row in board:
                cols.append(row[x])
            winners.append(cols)

        # Find all diagonal winning paths.
        winners.append([x[i] for i, x in enumerate(board)])
        winners.append([x[-i-1] for i, x in enumerate(board)])

        # Iterate through winning paths to check if game is won.
        for item in winners:
            if all(item[0] == x and x != EMPTY_MARK for x in item):
                print "WINNER"
                return True

        # Check if there is a stalemate.
        if not EMPTY_MARK in self.board:
            print "STALEMATE!!!"
            return True

        # Game not over, return False.
        return False


    def _is_valid_move(self, position):
        return list(self.board).pop(position) == EMPTY_MARK


