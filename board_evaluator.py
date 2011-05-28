def detect_win(board):
    #check for horizontal win
    for y in range(3):
        player = board[y][0]
        if player != 0 and player == board[y][1] and player == board[y][2]:
            return player
    #check for vertical win
    for x in range(3):
        player = board[0][x]
        if player != 0 and player == board[1][x] and player == board[2][x]:
            return player
    #check for diagonal win
    player = board[1][1]
    if player != 0 and player == board[0][0] and player == board[2][2]:
        return player
    if player != 0 and player == board[0][2] and player == board[2][0]:
        return player
    #no wins found return 0
    return 0
