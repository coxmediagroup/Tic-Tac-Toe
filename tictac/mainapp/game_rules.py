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
       for x in range(0,8):
          if board[x] == "_" :
             temp = list(board)
             temp[x] = "0"
             if calc_game_over(temp):
               print "rule win"
               return x     
       
       # brute force  for all posible moves :
       #if next move makes him win take it
       for x in range(0,8):
          print "(",x,")",
          if board[x] == "_" :
             temp = list(board)
             temp[x] = "X"
             print x,temp
             if calc_game_over(temp):
               print "rule not loose"
               return x
          print "skip"
          
       #if center not taken, take it.
       if board[4] == "_":
          print "rule center if not taken"
          return 4    

     #otherwise, randomly take first open space
       while True:
          i = random.randrange(0,8)
          if board[i] == "_" :
             print "rule random"
             return i 
     
