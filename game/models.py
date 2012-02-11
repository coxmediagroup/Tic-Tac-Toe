# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from picklefield.fields import PickledObjectField

# Tic Tac Toe game board is a 3x3 array
# We represent the board with a string of nine characters
# The offset into the string for each board square is:
# 0 1 2
# 3 4 5
# 6 7 8

# There are 8 possible lines, containing 3 squares:
lines = ((0, 1, 2),
         (3, 4, 5),
         (6, 7, 8),
         (0, 3, 6),
         (1, 4, 7),
         (2, 5, 8),
         (0, 4, 8),
         (2, 4, 6))

# The center of the board is at:
center = 4

# The middle edges are at:
edges = (1, 3, 5, 7)

# The four corners (and their opposite corner) are at:
corners = ((0, 8), (2, 6), (6, 2), (8, 0))


class Game(models.Model):
    INCOMPLETE, WON, LOST, TIE = range(4)
    STATUS_CHOICES = (
        (INCOMPLETE, _('Not completed')),
        (WON, _('Won')),
        (LOST, _('Lost')),
        (TIE, _('Tie')))
    player = models.ForeignKey(User, related_name='games')
    started = models.DateTimeField(_('Started'), auto_now_add=True)
    ended = models.DateTimeField(_('Ended'), auto_now=True)
    status = models.SmallIntegerField(_('Game Status'),
                                      choices=STATUS_CHOICES,
                                      default=INCOMPLETE)
    board = PickledObjectField()
    symbol = models.CharField(max_length=1, default='X')

    def __unicode__(self):
        return u'Player %s, %s' % (self.user.get_full_name(), self.status)

    @property
    def machine_symbol(self):
        '''Return character symbol for machine player (opposite of humans)'''
        if self.symbol == 'X':
            return 'O'
        else:
            return 'X'

    def find_single(self, *line):
        '''Find a line with a single X or O (whichever is machine_symbol)'''
        state = 0
        for cell in line:
            if self.board[cell] == self.machine_symbol:
                state += 16
            elif self.board[cell] == self.symbol:
                state += 4
            else:
                state += 1
        if state == 18:
            return True
        else:
            return False

    def line_count(self, *line):
        '''Count number of X's and O's in a line'''
        state = 0
        for cell in line:
            if self.board[cell] == self.machine_symbol:
                state += 1
            elif self.board[cell] == self.symbol:
                state -= 1
        return state

    def winner(self):
        '''Count number of lines that have three in a row'''
        empty_count = 0
        for line in lines:
            count = self.line_count(*line)
            if count == 3: # Three machine fills
                self.status = self.LOST
                return line
            if count == -3: # Three human fills
                self.status = self.WON
                return line
            for cell in line:
                if self.board[cell] == ' ':
                    empty_count += 1
        if empty_count == 0:
            self.status = self.TIE
            return range(9)
        return None

    def win_lines(self, symbol):
        '''
        Count number of lines that have one empty square and two
        of `symbol`. This is used to search for forks.
        '''
        count = 0
        for line in lines:
            state = 0
            for cell in line:
                if self.board[cell] == symbol:
                    state += 1
                elif self.board[cell] == ' ':
                    pass
                else:
                    state -= 1
            if state == 2:
                count += 1  # Another win line found
            if count == 2:
                break # No need for further searching if we find 2
        return count

    def place_win(self):
        '''Rule 1: Play three in a row'''
        for line in lines:
            if self.line_count(*line) == 2: # Two machine fills, and one empty
                for cell in line:
                    if self.board[cell] == ' ':
                        self.board[cell] = self.machine_symbol
                        return cell
        return None

    def place_block(self):
        '''Rule 2: Block opponent two in a row'''
        for line in lines:
            if self.line_count(*line) == -2: # Two player fills, and one empty
                for cell in line:
                    if self.board[cell] == ' ':
                        self.board[cell] = self.machine_symbol
                        return cell
        return None

    def place_fork(self):
        '''Rule 3: Create a fork'''
        for cell in range(9):
            if self.board[cell] == ' ':
                self.board[cell] = self.machine_symbol
                count = self.win_lines(self.machine_symbol)
                if count >= 2: # We found 2 win lines, so play this for a fork
                    return cell
                self.board[cell] = ' ' # Restore back to original
        return None

    def place_fork_block(self):
        '''Rule 4: Block opponents fork'''
        # Look for lines with one machine symbol so
        # we can block a fork with 2 in row
        for line in lines:
            if self.find_single(*line): # One machine fill, and two empty
                # Add a speculative machine symbol to one of the blanks
                for cell1 in line:
                    if self.board[cell1] == ' ':
                        self.board[cell1] = self.machine_symbol
                        break
                # Add speculative player symbol to the other blank square
                for cell2 in line:
                    if self.board[cell2] == ' ':
                        self.board[cell2] = self.symbol
                        break
                if self.win_lines(self.symbol) < 2: # No fork with this play
                    self.board[cell2] = ' '; # Restore cell2 (player cell)
                    return cell1
                self.board[cell1] = ' '; # Restore cell1 (machine cell)
                self.board[cell2] = ' '; # Restore cell2 (player cell)
        return None

    def place_center(self):
        '''Rule 5: Play the center'''
        if self.board[center] != ' ':
            return None
        self.board[center] = self.machine_symbol
        return center

    def place_opposite_corner(self):
        '''Rule 6: If opponent is in the corner, play the opposite corner'''
        for corner in corners:
            cell1 = corner[0]
            cell2 = corner[1]
            if self.board[cell1] == self.symbol and self.board[cell2] == ' ':
                self.board[cell2] = self.machine_symbol
                return cell2
        return None

    def place_empty_corner(self):
        '''Rule 7: Play in a corner'''
        for corner in corners:
            cell = corner[0]
            if self.board[cell] == ' ':
                self.board[cell] = self.machine_symbol
                return cell
        return None

    def place_empty_side(self):
        '''Rule 8: Play in a middle square on any side'''
        for cell in edges:
            if self.board[cell] == ' ':
                self.board[cell] = self.machine_symbol
                return cell
        return None

    def place_empty(self):
        '''Play any empty square (should only be one)'''
        for cell in range(9):
            if self.board[cell] == ' ':
                self.board[cell] = self.machine_symbol
                return cell
        return None

    def machine_move(self):
        if self.place_win() is not None:
            return
        if self.place_block() is not None:
            return
        if self.place_fork() is not None:
            return
        if self.place_fork_block() is not None:
            return
        if self.place_center() is not None:
            return
        if self.place_opposite_corner() is not None:
            return
        if self.place_empty_corner() is not None:
            return
        if self.place_empty_side() is not None:
            return
        self.place_empty()
        # Error check: any empty squares is an error at this point
        #for cell in range(9):
        #    if self.board[cell] == ' ':
        #        assert 0
        return
