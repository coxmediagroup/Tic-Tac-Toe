# from django.db import models
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Board(object):
    '''A 3x3 Tic-Tac-Toe board

    The board is numbered from the top left corner:

    0|1|2
    -+-+-
    3|4|5
    -+-+-
    6|7|8

    The two players ('X', who goes first, and 'O', who goes second) take turns
    placing their mark in an empty square, until someone has three marks in a
    straight line (a win), or there are no more empty squares (a tie).

    For a lot more information, see:
    http://en.wikipedia.org/wiki/Tic-tac-toe
    '''
    # Position states
    BLANK = 0
    MARK_X = 1
    MARK_O = 2

    def __init__(self, state=0):
        '''
        Initialize the board

        Keyword arguments:
        state - The state of the board, or 0 (default) for a new game
        '''

        self.board = []
        init_state = state
        for i in range(9):
            mark = state % 3
            self.board.append(mark)
            state /= 3
        x_moves = len([1 for p in self.board if p == self.MARK_X])
        o_moves = len([1 for p in self.board if p == self.MARK_O])
        if state != 0:
            raise ValueError('Bad state {} - too big'.format(init_state))
        if x_moves < o_moves:
            err = 'Bad state {} - too many O moves'.format(init_state)
            raise ValueError(err)
        if x_moves > o_moves + 1:
            err = 'Bad state {} - too many O moves'.format(init_state)
            raise ValueError(err)

    def __str__(self):
        '''String representation of board'''

        fmt = '''\
{}|{}|{}
-+-+-
{}|{}|{}
-+-+-
{}|{}|{}'''
        s = {
            self.BLANK: ' ',
            self.MARK_X: 'X',
            self.MARK_O: 'O',
        }
        return fmt.format(*[s[x] for x in self.board])

    def state(self):
        '''Return the state number of the board'''
        state = 0
        for p in reversed(self.board):
            state = (state * 3) + p
        return state

    def next_mark(self):
        '''Return which player placed the next mark'''
        moves = len([1 for p in self.board if p != 0])
        if moves % 2:
            return self.MARK_O
        else:
            return self.MARK_X

    def next_moves(self):
        '''Return valid next moves'''
        return [i for i, p in enumerate(self.board) if p == 0]

    def winner(self):
        '''Returns the winner, or False if no winner

        Returns 1 (MARK_X) if X is the winner
        Returns 2 (MARK_O) if O is the winner
        '''
        return False
