from django.db import models
from datetime import datetime
from random import randrange

class ArrayField(models.CommaSeparatedIntegerField):
    """
    A simple field that makes an actual array out of the comma-separated
    integers.  This is a custom class created by me.  There may be a better
    way to do this, though...
    """
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, list):
            return value

        return [int(i.strip('[').strip(']').strip())
                for i in unicode(value).split(',')]

    def get_prep_value(self, value):
        return unicode(','.join(unicode(i) for i in value))

# Create your models here.
class Player(models.Model):
    name = models.TextField(null=False,unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    lastActive = models.DateTimeField('Last Active',default=datetime.now())

    def __unicode__(self):
        return self.name

class Game(models.Model):
    '''
    Please see the README for a little bit of an explanation for why this
    is probably tricky to follow.
    '''
    EMPTY = 0                   # empty board position specifier
    X = 1                       # "player" X's integer to put in the board
    O = 4                       # "player" O's integer to put in the board
    ROW1 = [0,1,2]              # Indexes into the board array
    ROW2 = [3,4,5]              # Indexes into the board array
    ROW3 = [6,7,8]              # Indexes into the board array
    COL1 =      [0,3,6]         # Indexes into the board array
    COL2 =      [1,4,7]         # Indexes into the board array
    COL3 =      [2,5,8]         # Indexes into the board array
    DIAG1 = [0,4,8]             # Indexes into the board array
    DIAG2 = [6,4,2]             # Indexes into the board array
    LINES = (ROW1, ROW2, ROW3, COL1, COL2, COL3, DIAG1, DIAG2)
    CENTER = 4                  # Board's center index
    CORNERS = [0,2,6,8]         # Board's corners
    EDGES = [1,3,5,7]           # Board's edges
    player1 = models.ForeignKey(Player, related_name='player1')
    player2 = models.ForeignKey(Player, null=True, related_name='player2')
    winner = models.ForeignKey(Player, null=True, related_name='winner')
    ended = models.BooleanField(default=False)
    turn = models.SmallIntegerField(default=0)
    board = ArrayField(max_length=9,
            default=[0, 0, 0, 0, 0, 0, 0, 0, 0])

    def __unicode__(self):
        """ Could make this a little better formatted"""
        return unicode(self.board[:3]) + "\n" +\
                unicode(self.board[3:6]) + "\n" +\
                unicode(self.board[6:9])

    def lineVals(self, line):
        return [self.board[i] for i in line]

    def playerTurn(self, player, index):
        """
        Handle a non-computer player turn.
        """
        self.turn += 1
        self.board[index] = player

    def nextTurn(self, player=X):
        """
        A method to make the computer's move, or sugget a move to a user.
        It returns True if this move resulted in a win, False otherwise.

        Note, this method was written to work generically for any "player,"
        as specified by that player's X/O character.  However, it does actually
        change the board, so it can't just suggest a move.

        Win or draw with the following strategry (courtesy of Wikipedia):

        1. Win: If the player has two in a row, play the third to get three in
           a row.
        2. Block: If the opponent has two in a row,play the third to block them
        3. Fork: Create an opportunity where you can win in two ways.
        4. Block opponent's fork:
          * Option 1: Create two in a row to force the opponent into
           defending, as long as it doesn't result in them creating a fork or
           winning. For example, if "X" has a corner, "O" has the center, and
           "X" has the opposite corner as well, "O" must not play a corner in
           order to win. (Playing a corner in this scenario creates a fork for
           "X" to win.)
          * Option 2: If there is a configuration where the opponent can fork,
           block that fork.
        5. Center: Play the center.
        6. Opposite corner: If the opponent is in the corner, play the opposite
           corner.
        7. Empty corner: Play in a corner square.
        8. Empty side: Play in a middle square on any of the 4 sides.
        """

        # Pick a random corner if this is the beginning
        self.turn += 1
        if self.turn == 1:
            cornerIndexes = (0, 2, 6, 8)
            i = randrange(0, 3, 1)
            self.board[cornerIndexes[i]] = player
            return False
        elif self.turn >= 10:
            # TODO: This should probably throw an error...
            return False

        otherPlayer = self.X if player == self.O else self.O

        # Try to win, check for two in a row
        win = 2*player
        for line in self.LINES:
            if self.sumAndSet(line, win, player):
                return True

        # Try to block the other player
        block = 2*otherPlayer
        for line in self.LINES:
            if self.sumAndSet(line, block, player):
                return False

        # Either try to fork, or block the opponent from forking.
        if self.forkTestAndSet(player, otherPlayer):
            return False

        # Fill in the center, if available
        if self.board[self.CENTER] == self.EMPTY:
            self.board[self.CENTER] = player
            return False

        # Fill in the corner caddy-corner to first corner 
        if self.turn == 3 and self.sumAndSet(self.DIAG1, self.X+self.O, player):
            return False
        if self.turn == 3 and self.sumAndSet(self.DIAG2, self.X+self.O, player):
            return False

        # Fill in the first available corner:
        for cornerIndex in self.CORNERS:
            if self.board[cornerIndex] == self.EMPTY:
                self.board[cornerIndex] = player
                return False

        # Fill in the first available corner:
        for edgeIndex in self.EDGES:
            if self.board[edgeIndex] == self.EMPTY:
                self.board[edgeIndex] = player
                return False

        # TODO: This should definitely throw an exception, since we didn't
        # make a move.
        return False

    def sumAndSet(self, line, goal, player):
        """
        See if the given line adds up to the goal, and then set the only
        empty board space to 'player' if the goal is met.

        This method assumes that there is only one empty space in the given
        line, which doesn't make it very general at all.  It's only
        used as a convenience method to either win, or block the opponent
        from winning.
        """
        zeroIndex = None
        s = 0
        for i in line:
            c = self.board[i]
            s += c
            if c == self.EMPTY:
                zeroIndex = i

        if s == goal:
            self.board[zeroIndex] = player
            return True

        return False

    def forkTestAndSet(self, player, otherPlayer):
        # Try to fork for this player:
        forkPositions = self.forkablePositions(player)
        if forkPositions:
            self.board[forkPositions[0]] = player
            return True

        # Try to block a fork from the other player. That is, try to create
        # two in a row, then make sure the blocking position that the opponent
        # has to use isn't a fork position.
        forkPositions = self.forkablePositions(otherPlayer)
        if not forkPositions:
            return False

        # Try to find a line that only has one of the player's characters,
        # and then fill in one that doesn't leave a fork position open.
        for line in self.LINES:
            if sum(self.lineVals(line)) == player:
                emptyPositions = []
                for i in line:
                    if self.board[i] == self.EMPTY:
                        emptyPositions.append(i)
                pos1 = emptyPositions[0]
                pos2 = emptyPositions[1]
                # If they're both fork positions, then find another
                # line to make the opponent block.
                if pos1 in forkPositions and pos2 in forkPositions:
                    continue
                if pos1 in forkPositions:
                    self.board[pos1] = player
                    return True
                else:
                    self.board[pos2] = player
                    return True
        return False

    def forkablePositions(self, player):
        """
        Look for a position that could be used to fork the board.
        I.E. there are at least two paths that contain square A, that each
        have exactly one "player" mark in them:
         X _ O     X ~ *
         _ O _     _ O _  Note, this second one would be covered by
         * _ X  or _ O X  the original step #2 blocking code

         This is relatively inefficient, but it's not really worth making
         it faster.
        """
        forkPositions = []
        for index, playerChar in enumerate(self.board):
            if playerChar != self.EMPTY:
                continue
            forkableLines = 0
            for line in self.LINES:
                if index in line and sum(self.lineVals(line)) == player:
                    forkableLines += 1
            if forkableLines == 2:
                forkPositions.append(index)

        return forkPositions

    def checkWinner(self, player):
        """
        Return True if the given player ('X' or 'O') is the winner for this
        game, False otherwise.

        Note the relatively easy math.  If the player has won, then one
        of the lines will add up to 3 times that player's integer specifier.
        """
        win = 3*player
        for line in self.LINES:
            if sum(self.lineVals(line)) == win:
                return True

        return False
