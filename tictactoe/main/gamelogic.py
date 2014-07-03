# I cannot claim responsibility, for writing these two functions. I came across them tonight
# while searching around for information on Zero Sum theory, and algorithms for this type of
# application. This is an eloquent a solution as I believe possible, and it holds up to tests.
# Sometimes it's better to borrow, than reinvent the wheel. :) Gives more time to focus on other 
# aspects of your own application. -Damon
    
def isWin(board):
    """
    GIven a board checks if it is in a winning state.
 
    Arguments:
          board: a list containing X,O or -.
 
    Return Value:
           True if board in winning state. Else False
    """
    for i in range(3):
        if len(set(board[i*3:i*3+3])) == 1 and board[i*3] != '-': return True
    for i in range(3):
       if (board[i] == board[i+3]) and (board[i] == board[i+6]) and board[i] != '-':
           return True
    if board[0] == board[4] == board[4] == board[8] == board[4] is not '-':
        return  True
    if board[2] == board[4] == board[4] == board[6] == board[4] is not '-':
        return  True
    return False
 
 
def nextMove(board,player):
    """
    Computes the next move for a player given the current board state and also
    computes if the player will win or not.
 
    Arguments:
        board: list containing X,- and O
        player: one character string 'X' or 'O'
 
    Return Value:
        willwin: 1 if 'X' is in winning state, 0 if the game is draw and -1 if 'O' is
                    winning
        nextmove: position where the player can play the next move so that the
                         player wins or draws or delays the loss
    """
    if len(set(board)) == 1: return 0,4
    nextplayer = 'X' if player=='O' else 'O'
    if isWin(board) :
        if player is 'X': return -1,-1
        else: return 1,-1
    res_list=[]
    c= board.count('-')
    if  c == 0:
        return 0,-1
    _list=[]
    for i in range(len(board)):
        if board[i] == '-':
            _list.append(i)
    for i in _list:
        board[i]=player
        ret,move=nextMove(board,nextplayer)
        res_list.append(ret)
        board[i]='-'
    if player == 'X':
        maxele=max(res_list)
        return maxele,_list[res_list.index(maxele)]
    else :
        minele=min(res_list)
        return minele,_list[res_list.index(minele)] 
