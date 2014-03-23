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
    is_complete = models.BooleanField(default=False)

    class Meta:
        abstract = True


class TicTacToe(Game):
    board = models.CharField(max_length=SIZE, default=DEFAULT_BOARD)
    move_count = models.PositiveIntegerField(null=True, blank=True)

    class Meta(Game.Meta):
        verbose_name = 'Tic Tac Toe'

    def __unicode__(self):
        return '{}'.format(self.board)

    def move(self, position=None, player=None):

        # Check if the game is still active.
        if self.is_complete:
            print "GAME ALREADY FINISHED"
            return False

        # Check if player var was passed, if so then it must be time to move
        # the players mark. Initiate the computer's turn once completed.
        if player:
            if int(position) <= len(self.board) and self._is_valid_move(position):
                self.board = list(self.board)
                self.board.pop(position)
                self.board.insert(position, PLAYER_MARK)
                self.board = ''.join(self.board)
                self.save()

                # Check if the game is complete, if not then computers turn.
                if self._is_complete():
                    print "GAME OVER"
                else:
                    self.move()
            else:
                print 'OH NOEZ NOT VALID MOVE'
        else:
            # Add logic here so that computer always wins
            # 1) Check if player has more than 1 mark, if not, move to center
            # 2) If player has more than 1 mark, block any attempt at winning
            print "COMPUTER TURN"
            marks = self.board.count(PLAYER_MARK)
            print marks
            if marks < 2 and self._center_empty:
                self.board = list(self.board)
                self.board.pop(self._center_position)
                self.board.insert(self._center_position, COMPUTER_MARK)
                self.board = ''.join(self.board)
                self.save()

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
                self.is_complete = True
                self.save()
                return True

        # Check if there is a stalemate.
        if not EMPTY_MARK in self.board:
            print "STALEMATE!!!"
            self.is_complete = True
            self.save()
            return True

        # Game not over, return False.
        return False

    def _is_valid_move(self, position):
        return list(self.board).pop(position) == EMPTY_MARK

    @property
    def _center_empty(self):
        return self.board[self._center_position] == EMPTY_MARK

    @property
    def _center_position(self):
        return self.center(SIZE)

    @staticmethod
    def center(size):
        return ((SIZE**2) - 1) / 2

