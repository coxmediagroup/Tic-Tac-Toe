import random

def  calc_game_over(board):
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
          
       #if corners not taken, take one
       for x in [0,2,6,8]:
          if board[x] == "_":
             return x
             
       #otherwise, randomly take first open space
       while True:
          i = random.randrange(0,9)
          if board[i] == "_" :
             return i 
     
