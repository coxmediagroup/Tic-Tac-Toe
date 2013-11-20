
EMPTY_SYM='-'
X_CHAR='x'
O_CHAR='o'

from random import randint
import random
from ComputerPlayer import ComputerPlayer, RandomPlayer
import copy
from utils import prnt
from utils import debug_print as d_pr
from utils import console_print

class TicTacToe_Board(object):
    
    
    
    def __init__(self, SubRandomForHuman=False):
        
        #init empty board
        self.board_array=[[EMPTY_SYM,EMPTY_SYM, EMPTY_SYM],
                          [EMPTY_SYM,EMPTY_SYM, EMPTY_SYM],
                          [EMPTY_SYM,EMPTY_SYM, EMPTY_SYM]] 
        random.seed()
        
        self.x_or_o_arr = ['x', 'o']
        
        self.the_winner = None
        
        #turn is random at init time
        self.whose_turn=self.x_or_o_arr[randint(0,1)]
        
        console_print('First turn goes to player ' + self.whose_turn)
        
        self.human_player_x_or_o = self.x_or_o_arr[randint(0,1)]
        
        console_print ('Human player is ' + self.human_player_x_or_o)
        
        self.c_player_x_or_o = 'x' if self.human_player_x_or_o == 'o' else 'o'
        
        console_print ('Computer player is ' + self.c_player_x_or_o)
        
        self.c_player = ComputerPlayer(self.c_player_x_or_o, self)
        
        self.r_player = None
        
        #instead of playing against a human, play against a really dumb computer who make random moves
        #used for testing
        if SubRandomForHuman:
            self.r_player = RandomPlayer(self)
        
        
        self.GameStatus = 'Started'
    
    def SetGameOver(self, the_winner):
        self.GameStatus = 'Over'
        self.the_winner = the_winner
    
    
    def ChangeTurn(self):
        if self.whose_turn == 'o':
            self.whose_turn = 'x'
        else:
            self.whose_turn = 'o'
    
    #returns 'x' or 'o' or 'None' if x wins, o wins , or nobody has won yet
    @staticmethod
    def IsWinningBoard_static(a_board_array):
        
        #check rows, then cols then diagonals if are either x's or 'o's (but not Empty_sym)
        for r in range(0,2+1):
            if a_board_array[r][0]==a_board_array[r][1]==a_board_array[r][2]!=EMPTY_SYM:
                return a_board_array[r][0]
        #columns
        for c in range(0,2+1):
            if a_board_array[0][c]==a_board_array[1][c]==a_board_array[2][c]!=EMPTY_SYM:
                return a_board_array[0][c]
            
        #diagonals
        
        if (a_board_array[0][0]==a_board_array[1][1]==a_board_array[2][2]
            !=EMPTY_SYM) or (\
                a_board_array[2][0]==a_board_array[1][1]==a_board_array[0][2]!=EMPTY_SYM):
            return a_board_array[1][1] #middle square 
        
        #nobody won, return none
        return None
    
    
    def IsWinningBoard(self):
        return TicTacToe_Board.IsWinningBoard_static(self.board_array)
        
        
    def MakeMove(self, row_and_col, specific_player=None):
        
        
        #move is made by the person whose turn it is, unless overriden by param specific player
        
        specific_player = self.whose_turn if specific_player == None else specific_player 
        
        row=row_and_col[0]
        col=row_and_col[1]
        
        if self.board_array[row][col]!=EMPTY_SYM:
            raise Exception("cannot make move onto a non-blank square")
        
        self.board_array[row][col]=specific_player
        
        if self.IsWinningBoard() or len(self.GetEmptySquares())==0:
            self.GameStatus = 'Over'
            self.the_winner = self.IsWinningBoard() if self.IsWinningBoard() else 'tie'
            
        
        self.ChangeTurn()
    
        return 
    
    
    # returns a list of winning moves that the given player could make to win
    #given the current board configuration
    def GetWinningMovesFor(self, which_player):
        
        empty_sq = self.GetEmptySquares()
       
        winning_moves = []
        for_whom = ''
        
        if which_player == 'computer':
            for_whom=self.c_player_x_or_o
        else:
            for_whom = self.human_player_x_or_o
        # for each empty square, simulate the opponent going there
        # and if he wins, this is a winning move for him
        for sq in empty_sq:
            outcome=self.GetOutcomeOfMoveSequence([{'player': for_whom,  'move': sq}])
            # if
            if outcome == for_whom:
                winning_moves.append(sq)
        
        return winning_moves
    
    #given a sequence of moves ( a move is a square paired with which player is making the move)
    #return the outcome which is either 'x', 'o' or None depending if somebody won
    def GetOutcomeOfMoveSequence(self, move_sequence):
        
        
    
        
        board_copy = copy.deepcopy(self)
        
        for m in move_sequence:
            board_copy.MakeMove(m['move'], specific_player=m['player'])
            
            outcome=board_copy.IsWinningBoard()
            
            #if somebody won, return the outcome
            if (outcome != None):
                return outcome
      
        
        # return last outcome
        return outcome
    
    
    #makes a copy of the boar and simulates making a sequence of moves on the board
    
    def GetBoardWithSimulatedMove(self, move_sequence):
        
        board_copy = copy.deepcopy(self)
        
        for m in move_sequence:
            board_copy.MakeMove(m['move'], specific_player=m['player'])
            
        return board_copy
    
    #prints the board to the console
    
    def PrintBoardToConsole(self):
        
        
        console_print()
        console_print()
        
        for r in self.board_array:
            for c in r:
                prnt(c + ' ')
            
            prnt('\n')
    
    

    #return list of the squares on the board that are still empty 
    def GetEmptySquares(self):
        
        empty_list = []
        
        for r in range(0,2+1):
            for c in range(0,2+1):
                if self.board_array[r][c] == EMPTY_SYM:
                    empty_list.append([r,c])
        
        return empty_list
        
    

        