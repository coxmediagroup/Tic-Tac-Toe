from Board import TicTacToe_Board
import re
from utils import debug_print as d_pr
from utils import console_print

def get_move_from_user(the_board):
        
    if the_board.r_player == None:
        
        console_print("It's your move:")
        console_print("Pls enter row (1-3) and column (1-3) separated by comma (e.g. 1,1 for top right corner):")
        console_print() 
        move_spec = raw_input()
    
        if not IsValidMove(move_spec,the_board):
            return None
    
        return ConvertToMove(move_spec)
    
    #if we're using a computer randomizer instead of a human
    else:
        return the_board.r_player.GetNextMove()

def ConvertToMove(move_spec):
    
    row, col = move_spec.split(',')
    return [int(row)-1, int(col)-1]
    

def IsValidMove(move_spec, the_board):
    if re.match('^[1-3],[1-3]$', move_spec ) == None:
        return False
    
    converted_move = ConvertToMove(move_spec)
    
    if converted_move not in the_board.GetEmptySquares():
        return False
    
    return True

def StartNewGame(UseRandom=False):
    the_board = TicTacToe_Board(SubRandomForHuman=UseRandom)
    
    return main_loop(the_board)


    

def main_loop(the_board):
    
    while the_board.GameStatus != 'Over':
    
      if the_board.whose_turn == the_board.c_player_x_or_o:
          the_board.c_player.MakeMove()
        
      if the_board.GameStatus == 'Over':
          break
      
      the_board.PrintBoardToConsole()
      user_move=get_move_from_user(the_board)
    
      while user_move == None:
          print 'Invalid move...pls try again with x,y where x is row and y is column. Both should be either 1,2, or 3 and the square must be empty.'
          user_move=get_move_from_user(the_board) 
    
      the_board.MakeMove(user_move)
      
      d_pr('User chose square at ' + str(user_move))
    
        
    
    
    the_board.PrintBoardToConsole()
    
    if the_board.the_winner != 'tie':
        console_print('Winner is ' + the_board.the_winner)
    
    console_print() 
    
    winner_val = 'Unset'
    
    if the_board.the_winner == the_board.c_player_x_or_o:
        winner_val = 'Computer'
        console_print('The computer won.')
    if the_board.the_winner == the_board.human_player_x_or_o:
        winner_val = 'Human'
        console_print( 'You won.')
    if the_board.the_winner == 'tie':
        console_print ("It's a tie")
        winner_val = 'Tie'
    
    return winner_val 

def main():
    
    StartNewGame()
    
    
    
if __name__ == '__main__':
    #print 'in main'
    main()
    