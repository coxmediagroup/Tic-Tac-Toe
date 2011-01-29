'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski (krzysztof.tarnowski@ymail.com)
'''

import itertools

import engine

def board_to_str(board):
    ''' '''       
 
    def value_to_char(value):
        ''' '''
        if value == engine.P1: return 'X'
        if value == engine.P2: return 'O'
        
        return ' '

    fields = [value_to_char(value) for value in list(itertools.chain.from_iterable(board))]
    
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