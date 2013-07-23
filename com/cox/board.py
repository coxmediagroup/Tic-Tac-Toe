'''
Created on Jul 22, 2013

@author: christie
'''

class board(object):
    '''
    class that represents board
    '''


    def __init__(self, **kwargs):
        '''
        initialize board as two-d list
        '''
        self.board = [['-','-','-'],
                      ['-','-','-'],
                      ['-','-','-']
                      ]
        self.human_letter = kwargs.get('human', '')
        self.computer_letter = kwargs.get('computer', '')
    
    def print_board(self):
        """
        print current board state
        """        
        # This function prints out the board that it was passed.
        # "board" is a list of 10 strings representing the board (ignore index 0)        
        print(' ' + self.board[2][0] + ' | ' + self.board[2][1] + ' | ' + self.board[2][2])        
        print('-----------')        
        print(' ' + self.board[1][0] + ' | ' + self.board[1][1] + ' | ' + self.board[1][2])        
        print('-----------')        
        print(' ' + self.board[0][0] + ' | ' + self.board[0][1] + ' | ' + self.board[0][2])