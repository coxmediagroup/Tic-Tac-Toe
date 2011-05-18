import random
'''
      The tic tac toe "board" is represented by a list :
       [0,1,2,3,4,5,6,7,8]
           
       0 | 1 | 2
       3 | 4 | 5
       6 | 7 | 8
        
       With 3 possible states for any given element on the list:
       X = Human player
       O = Computer player
       _ = empty space
       
       The game ends with a tie when there are no empty spaces left to play 
       or when somebody wins (calc_game_over = True )
'''


def  calc_game_over(board):
       '''if any of the 9 wining positions has been played
          then declare a game over.
          0,1,2 would be top horizontal
          0,4,8 would be diagonal
          0,3,6 hould be vertical
          and so on ...
       '''
       if board[0]==board[1]==board[2]!="_"  or \
          board[0]==board[3]==board[6]!="_"  or \
          board[0]==board[4]==board[8]!="_"  or \
          board[6]==board[7]==board[8]!="_"  or \
          board[2]==board[5]==board[8]!="_"  or \
          board[2]==board[4]==board[6]!="_"  or \
          board[2]==board[4]==board[6]!="_"  or \
          board[1]==board[4]==board[7]!="_"  or \
          board[3]==board[4]==board[5]!="_" :        
          return True
       else: 
         return False
         
         
def  calc_computer_move(board):
       ''' Slow but simple rule engine for calculating
           the next best move (for the computer player)          
       '''
       # brute force  for all posible moves :
       #if next move makes *me* win, take it.
       for x in range(0,9):
          if board[x] == "_" :
             temp = list(board)
             temp[x] = "0"
             if calc_game_over(temp):
               return x     
       
       # brute force  for all posible moves :
       #if next move makes him win take it
       for x in range(0,9):
          if board[x] == "_" :
             temp = list(board)
             temp[x] = "X"
             if calc_game_over(temp):
               return x
          
       #if center not taken, take it.
       if board[4] == "_":
          return 4    
       
       #if opposite corners, pick an edge
       if (board[0] == board[8] == "X") or (board[2] == board[6] == "X"):
          for x in [1,3,5,7]:
             if board[x] == "_":
                return x
          
          
       #if corners not taken, take one
       for x in [0,2,6,8]:
          if board[x] == "_":
             return x
             
       #otherwise, randomly take first open space
       while True:
          i = random.randrange(0,9)
          if board[i] == "_" :
             return i 
     
