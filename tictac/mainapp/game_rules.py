# Box states: 
# 0 empty
# 1 player
# 2 computer

def test_valid_move(board,move):
    """ test if the move is valid
    """
   #test for already used space 
    if board[move] != "_" :
       return False
    else :
       return True
           
