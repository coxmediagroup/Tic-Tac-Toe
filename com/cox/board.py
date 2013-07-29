'''
Created on Jul 22, 2013

@author: christie
'''

class board(object):
    """
    class that represents board
    """


    def __init__(self, **kwargs):
        """
        initialize board as two-d list
        and set default value on each positions
        """
        self.board = [['*','*','*'],
                      ['*','*','*'],
                      ['*','*','*']
                      ]
        self.players = {'human': kwargs.get('human', ''),
                        'computer': kwargs.get('computer', '')
                        }
    
    def print_board(self):
        """
        print all markings on the board 
        """    
        print(' ' + self.board[2][0] + ' | ' + self.board[2][1] + ' | ' + self.board[2][2])        
        print('-----------')        
        print(' ' + self.board[1][0] + ' | ' + self.board[1][1] + ' | ' + self.board[1][2])        
        print('-----------')        
        print(' ' + self.board[0][0] + ' | ' + self.board[0][1] + ' | ' + self.board[0][2])
    
    def move(self, player, position):
        """
        mark position for a player on the board
        """
        row,col = list(position)        
        self.board[int(row)][int(col)] = self.players[player]    
    
    def is_space_available(self,position):
        """
        check a position on the board if it is
        already marked
        """
        row,col = list(position)
        return (self.board[int(row)][int(col)] == '*')
    
    def is_winner(self, player):
        """
        checks the board for the winning pattern
        for a player
        player =  computer or human        
        """
        return ((self.board[0][0] == self.players[player] and self.board[0][1] == self.players[player] and self.board[0][2] == self.players[player]) or
                (self.board[1][0] == self.players[player] and self.board[1][1] == self.players[player] and self.board[1][2] == self.players[player]) or
                (self.board[2][0] == self.players[player] and self.board[2][1] == self.players[player] and self.board[2][2] == self.players[player]) or
                (self.board[0][0] == self.players[player] and self.board[1][0] == self.players[player] and self.board[2][0] == self.players[player]) or
                (self.board[0][1] == self.players[player] and self.board[1][1] == self.players[player] and self.board[2][1] == self.players[player]) or
                (self.board[0][2] == self.players[player] and self.board[1][2] == self.players[player] and self.board[2][2] == self.players[player]) or
                (self.board[0][0] == self.players[player] and self.board[1][1] == self.players[player] and self.board[2][2] == self.players[player]) or
                (self.board[0][2] == self.players[player] and self.board[1][1] == self.players[player] and self.board[2][0] == self.players[player])
                )
    
    def is_board_full(self):
        """
        check if board is full
        """
        for i in range(3):
            for j in range(3):
                if self.is_space_available(str(i)+str(j)):
                    return False
        return True
    
    def reset(self):
        """
        reset all positions on the board
        """
        for i in range(3):
            for j in range(3):
                self.board[i][j] = '*'