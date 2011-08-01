import random, math

ID_PLAYER = 0
ID_COMPUTER = 1
ID_TIE = 2

FLAG_SAFE = 0
FLAG_UNSAFE = 1
FLAG_WIN = 2

# plot player on board and check for win
# return False if the spot is already taken
def makeMove(board, x, y):
    
    if board.isVacant((x,y)):
        board.makeMove((x,y), ID_PLAYER)
        return True
    else:
        return False

# calculate the computer's next move
# return tuple (x,y) containing the computer's suggested move
def getMove(board):
    
    # is there a spot to move?
    if board.isFull():
        return False
    
    if board.isEmpty():
        # this is the first move, just choose a random point
        while True:
            x = random.randint(0,2);
            y = random.randint(0,2);
            return (x,y)
    
    # here's the idea
    # for each move the computer can make, calculate all outcomes (win, loss, tie)
    # trace backwards from the outcomes, make sure the computer doesn't
    # make a move that can lead to a losable outcome
    # the key is to flag outcomes where the computer can lose (assume the player will go for the win)
    safe_moves = []
    win_moves = []
    for cell in board.getEmptyCells():
        flag = seeOutcomeForCell(board, cell)
        if flag == FLAG_SAFE:
            safe_moves.append(cell)
        elif flag == FLAG_WIN:
            win_moves.append(cell)
    
    # select from safe moves, winning moves take precedence
    if len(win_moves):
        return win_moves[0]
    else:
        return safe_moves[0]
    
    
    return False # this case should never happen

# see if the player/computer (specified by playerId) can win the game on the next turn
def checkForWinningMove(board, playerId):
    for cell in board.getEmptyCells():
        board.makeMove(cell, playerId)
        win = board.checkForWin(playerId)
        board.clear(cell)
        if win:
            return True
    
    return False

def seeOutcomeForCell(board, cell):
    board.makeMove(cell, ID_COMPUTER)
    
    win = board.checkForWin(ID_COMPUTER)
    if win:
        flag = FLAG_WIN
    else:
        flag = seeOutcome(board, ID_PLAYER)
    
    board.clear(cell)
    return flag

# base case: win, loss or tie
# return FLAG_SAFE for tie
# return FLAG_UNSAFE for loss
# return FLAG_WIN to win
# node is cleared (set to safe) if there is a another path on the node that leads to a safe/win flag
def seeOutcome(board, currentPlayerId):
    win = checkForWinningMove(board, currentPlayerId)
    if win:
        if currentPlayerId == ID_PLAYER:
            return FLAG_UNSAFE
        else:
            return FLAG_WIN
    
    if board.isFull():
        return FLAG_SAFE
    
    if currentPlayerId == ID_PLAYER:
        flag = FLAG_SAFE
        win = True
        for cell in board.getEmptyCells():
            board.makeMove(cell, ID_PLAYER)
            f = seeOutcome(board, ID_COMPUTER)
            board.clear(cell)
            if f == FLAG_UNSAFE:
                flag = f
            if f != FLAG_WIN:
                win = False
    else:
        flag = FLAG_UNSAFE
        win = False
        for cell in board.getEmptyCells():
            board.makeMove(cell, ID_COMPUTER)
            f = seeOutcome(board, ID_PLAYER)
            board.clear(cell)
            if f != FLAG_UNSAFE:
                flag = f
    
    if win:
        flag = FLAG_WIN
    return flag

def isGameOver(board):
    if board.checkForWin(ID_PLAYER):
        return ID_PLAYER
    elif board.checkForWin(ID_COMPUTER):
        return ID_COMPUTER
    elif board.isFull():
        return ID_TIE
    else:
        return False
