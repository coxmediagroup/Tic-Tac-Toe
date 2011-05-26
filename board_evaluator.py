def detect_win(board):
    #check for horizontal win
    for y in range(3):
        player = board[y][0]
        if player == board[y][1] and player == board[y][2]:
            return (True, player)
    #check for vertical win
    for x in range(3):
        player = board[0][x]
        if player == board[1][x] and player == board[2][x]:
            return (True, player)
    #check for diagonal win
    player = board[1][1]
    if player == board[0][0] and player == board[2][2]:
        return (True, player)
    if player == board[0][2] and player == board[2][0]:
        return (True, player)
    #no wins found return False
    return (False, None)

def detect_cat(board):
    '''warning: this function will denote wins as cats if they have filled all
nine spaces'''
    #check to see if all spaces are filled
    for y in range(3):
        for x in range(3):
            if board[y][x] is None:
                return False
    return True
