#!/usr/bin/env python

players = ('X', 'O')

wins = (
    # Horizontal
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    # Vertical
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    # Diagonal
    (0, 4, 8),
    (2, 4, 6),
)

def _reduce_win(x, y):
    '''A win occurs when all three spaces in a possible win configuration
    are equal.'''

    if x == y:
        return x
    return False

class Board(object):
    def __init__(self):
        self.spaces = range(9)

    def __repr__(self):
        return '''
%s | %s | %s
--+---+--
%s | %s | %s
--+---+--
%s | %s | %s
        '''.strip() % tuple(self.spaces)

    def __unicode__(self):
        return unicode(self.__repr__())

    def isEmpty(self, index):
        raise NotImplementedError('Implement test for an empty square.')

    def move(self, index, player):
        raise NotImplementedError('Implement the ability for a player to move.')
    def winner(self):
        '''Return who the winner is, if any.'''
        for win in wins:
            winner = reduce(_reduce_win, map(self.spaces.__getitem__, win))
            if winner:
                return winner
        return None

    def available_moves(self):
        '''Return available moves.'''

        # A move is available if it's still an integer
        return filter(lambda x: isinstance(x, int), self.spaces)
