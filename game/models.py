# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Game(models.Model):
    INCOMPLETE, WON, LOST, TIE = range(4)
    STATUS_CHOICES = (
        (INCOMPLETE, _('Not completed')),
        (WON, _('Won')),
        (LOST, _('Lost')),
        (TIE, _('Tie')))
    user = models.ForeignKey(User, related_name='games')
    started = models.DateTimeField(_('Started'), auto_now_add=True)
    ended = models.DateTimeField(_('Ended'), auto_now=True)
    status = models.SmallIntegerField(_('Game Status'),
                                      choices=STATUS_CHOICES,
                                      default=INCOMPLETE)
    board = models.CharField(max_length=9)

    def __unicode__(self):
        return u'Player: %s %s' % (self.user.get_full_name(), self.status)

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

    # The middle sides are at:
    sides = (1, 3, 5, 7)

    # The four corners (and their opposite corner) are at:
    corners = ((0, 8), (2, 6), (6, 2), (8, 0))

    def place_win(self):
        '''Rule 1: Play three in a row'''
        for line in lines:
            state = 0
            for cell in line:
                state += self.board[cell]
            if state == 2:
                for cell in line:
                    if self.board[cell] == 0:
                        self.board[cell] = 1
                        return cell
        return None

    def place_block(self):
        '''Rule 2: Block opponent two in a row'''
        for line in lines:
            state = 0
            for cell in line:
                state += self.board[cell]
            if state == -2:
                for cell in line:
                    if self.board[cell] == 0:
                        self.board[cell] = 1
                        return cell
        return None

    def place_fork(self):
        '''Rule 3: Create a fork'''
        return None

    def place_fork_block(self):
        '''Rule 4: Block opponents fork'''
        return None

    def place_center(self):
        '''Rule 5: Play the center'''
        if self.board[center]:
            return None
        self.board[center] = 1
        return center

    def place_opposite_corner(self):
        '''Rule 6: If opponent is in the corner, play the opposite corner'''
        for corner in corners:
            cell1 = corner[0]
            cell2 = corner[1]
            if self.board[cell1] == -1 and self.board[cell2] == 0:
                self.board[cell2] = 1
                return cell2
        return None

    def place_empty_corner(self):
        '''Rule 7: Play in a corner'''
        for corner in corners:
            cell = corner[0]
            if self.board[cell] == 0:
                self.board[cell] = 1
                return cell
        return None

    def place_empty_side(self):
        '''Rule 8: Play in a middle square on any side'''
        for cell in sides:
            if self.board[cell] == 0:
                self.board[cell] = 1
                return cell
        return None
