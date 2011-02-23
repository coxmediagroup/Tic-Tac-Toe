'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski (krzysztof.tarnowski@ymail.com)
'''

import engine


def board_to_str(board):
    ''' Pretty prints the game board.

    Args:
        board: A 3x3 numpy array
     '''

    def value_to_char(value):
        ''' Converts constants representing players on a game board to char
            representation.

        Args:
            value: A constant representing a player.

        Returns:
            Either 'X', 'O' or space character.
        '''
        if value == engine.P1:
            return 'X'
        if value == engine.P2:
            return 'O'

        return ' '

    fields = [value_to_char(value) for value in board.flat]

    board_str = \
'''    0   1   2
  +---+---+---+
0 | {0} | {1} | {2} |
  +---+---+---+
1 | {3} | {4} | {5} |
  +---+---+---+
2 | {6} | {7} | {8} |
  +---+---+---+'''.format(*fields)

    return board_str
