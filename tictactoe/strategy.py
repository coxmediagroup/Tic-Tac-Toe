'''
Defines Tic-Tac-Toe strategies

Each strategy has a 'next_move' method to decide the next move
'''

from random import choice as random_choice


class RandomStrategy(object):
    '''Randomly picks next move'''

    def next_move(self, board):
        return random_choice(board.next_moves())
