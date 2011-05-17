def  calc_computer_move(board):
       return 4    

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

