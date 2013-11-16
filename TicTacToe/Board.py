
EMPTY_SYM='-'
X_CHAR='x'
O_CHAR='o'

from random import randint
import random

class TicTacToe_Board(object):
    
    def __init__(self):
        
        #init empty board
        self.board_array=[[EMPTY_SYM,EMPTY_SYM, EMPTY_SYM],
                          [EMPTY_SYM,EMPTY_SYM, EMPTY_SYM],
                          [EMPTY_SYM,EMPTY_SYM, EMPTY_SYM]] 
        random.seed()
        
        self.whose_turn=randint(0,1)
        
    
    
    #returns 'x' or 'o' or 'None'
    @staticmethod
    def IsWinningBoard(a_board_array):
        
        #check rows, then cols then diagonals if are either x's or 'o's (but not Empty_sym)
        for r in range(0,2):
            if a_board_array[r][0]==a_board_array[r][1]==a_board_array[r][2]!=EMPTY_SYM:
                return a_board_array[r][0]
        #columns
        for c in range(0,2):
            if a_board_array[0][c]==a_board_array[1][c]==a_board_array[2][c]:
                return a_board_array[0][c]
            
        #diagonals
        
        if (a_board_array[0][0]==a_board_array[1][1]==a_board_array[2][2]
            !=EMPTY_SYM) or (\
                a_board_array[2][0]==a_board_array[1][1]==a_board_array[0][2]!=EMPTY_SYM):
            return a_board_array[1][1] #middle square 
        
        #nobody won, return none
        return None
    
    
        