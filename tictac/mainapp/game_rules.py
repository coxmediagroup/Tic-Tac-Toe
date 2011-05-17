# Play states: 
#    _ empty
#    X player
#    0 computer

#def test_valid_move(board,move):
#    """ test if the move is valid
#    """
#   #test for already used space 
#    if board[move] != "_" :
#       return False
#    else :
#       return True

def  calc_computer_move(board):
       return 4    

def  calc_game_over(board):
       if board[0] == "X":
         return True
       else: 
         return False

