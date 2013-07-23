'''
Created on Jul 22, 2013

@author: christie
'''

class board(object):
    '''
    class that represents board
    '''


    def __init__(self):
        '''
        initialize board as two-d list
        '''
        self.board = [['-','-','-'],
                      ['-','-','-'],
                      ['-','-','-']]
    def print_board(self):
        """
        print current board state
        """
        print self.board[0]
        print self.board[1]
        print self.board[2]