import json

from django.db import models


EMPTY_MARK = '-'
COMPUTER_MARK = 'O'
PLAYER_MARK = 'X'
SIZE = 3
DEFAULT_BOARD = EMPTY_MARK * SIZE**2

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
        """
        Object method to initiate a move in the Tic-Tac-Toe game.

        First runs a few sanity checks to make sure it's not a completed game
        and that the method was initialized correctly.

        If position and player are given then the turn must be for the player, if
        neither are given then the turn must be for the computer.

        After each player turn, the computer automatically gets a turn. The computer
        determines it's next move based on the following logic:

        1) Check if player has more than 1 mark, if not, place at center.
        2) If the player has more than one mark, block any attempt at win.
        3) If no attempt at win, place mark in one of the corners.

        """
        # Check if the game is still active.
        if self.is_complete:
            print "GAME ALREADY FINISHED"
            return False

        # Check if player var was passed, if so then it must be time to move
        # the players mark. Initiate the computer's turn once completed.
        if player:
            if int(position) <= len(self.board) and self._is_valid_move(position):
                self._place_mark(position, PLAYER_MARK)

                # Now it is the computers turn.    
                self.move()
            else:
                print 'OH NOEZ NOT VALID MOVE'
        else:
            # Check if player has more than 1 mark, if not, move to center.
            marks = self.board.count(PLAYER_MARK)
            
            if marks < 2 and self._center_empty:
                self._place_mark(self._center_position, COMPUTER_MARK)

            else:
                # Make winning move or block the player from his winning move, then check
                # to see if the game was won and if so set is_complete = True.
                if not self.winning_move(COMPUTER_MARK) or not self.winning_move(PLAYER_MARK):
                    # Otherwise just pick an empty space and move there.
                    # TODO: Choose corners or random space.
                    position = self.board.find(EMPTY_MARK)
                    self._place_mark(position, COMPUTER_MARK)

            if self._game_won:
                self.is_complete = True
                self.save()
                print "GAME OVER - COMPUTER WINS!"

        return self.board

    def winning_move(self, player_mark):
        next_move = []
        for position, mark in enumerate(self.board):
            if mark == EMPTY_MARK:
                old = self.board
                self._place_mark(position, player_mark)
                if self._game_won:
                    next_move.append(position)
                    break
                self.board = old
        
        if len(next_move) > 0:
            print next_move
            self._place_mark(next_move[0], COMPUTER_MARK)
            return True

        return False

    def _place_mark(self, position, mark):
        self.board = list(self.board)
        self.board.pop(position)
        self.board.insert(position, mark)
        self.board = ''.join(self.board)
        return self.save()

    @property
    def _winning_paths(self):
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

        return winners

    @property
    def _game_won(self):
        # Iterate through winning paths to check if game is won.
        won = False

        for path in self._winning_paths:
            if all(path[0] == x and x != EMPTY_MARK for x in path):
                won = True
                break

        # Check if there is a stalemate.
        if not EMPTY_MARK in self.board and not won:
            won = True

        # Game not over, return False.
        return won

    def _is_valid_move(self, position):
        return list(self.board).pop(position) == EMPTY_MARK

    @property
    def _get_corners(self):
        # Could get this programatically but simple enough to just return them.
        return [self.board[i] for i in (0, 2, 6, 8)]

    @property
    def _center_empty(self):
        return self.board[self._center_position] == EMPTY_MARK

    @property
    def _center_position(self):
        return self._center(SIZE)

    @staticmethod
    def _center(size):
        return ((SIZE**2) - 1) / 2

