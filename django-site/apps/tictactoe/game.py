import random, math

ID_PLAYER = 1
ID_COMPUTER = 2

FLAG_SAFE = 0
FLAG_UNSAFE = 1
FLAG_WIN = 2

class Result():
    pass

def makemove(matrix, x, y):
    result = Result()
    if matrix[x][y]:
        return False
    else:
        result.x = x
        result.y = y
        return result

def getmove(matrix):
    result = Result()
    
    # is there a spot to move?
    emptyMatrix = True
    fullMatrix = True
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == 0:
                fullMatrix = False
            else:
                emptyMatrix = False
    
    if fullMatrix:
        return False
    
    if emptyMatrix:
        # this is the first move, just choose a random point
        while True:
            x = random.randint(0,2);
            y = random.randint(0,2);
            if matrix[x][y] == 0:
                result.x = x
                result.y = y
                break
        return result
    
    # here's the idea
    # for each move the computer can make, calculate all outcomes (win, loss, tie)
    # trace backwards from the outcomes, make sure the computer doesn't
    # make a move that can lead to a losable outcome
    # the key is to flag outcomes where the computer can lose (assume the player will go for the win)
    nextX = 0
    nextY = 0
    max = 0
    first = True
    flag_matrix = [[0,0,0],[0,0,0],[0,0,0]]
    safe_moves = []
    win_moves = []
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == 0:
                flag = seeOutcomeForXY(matrix, x, y)
                flag_matrix[x][y] = flag
                #if flag != FLAG_UNSAFE:
                #    safe_moves.append((x,y))
                if flag == FLAG_SAFE:
                    safe_moves.append((x,y))
                elif flag == FLAG_WIN:
                    win_moves.append((x,y))
    
    #print len(safe_moves)
    print flag_matrix
    if len(win_moves):
        m = random.randint(0,len(win_moves)-1)
        result.x = win_moves[m][0]
        result.y = win_moves[m][1]
    else:
        m = random.randint(0,len(safe_moves)-1)
        result.x = safe_moves[m][0]
        result.y = safe_moves[m][1]
    
    
    return result

# see if the player/computer (specified by playerId) can win the game on the next turn
def checkForWinningMove(matrix, playerId):
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == 0:
                matrix[x][y] = playerId
                result = checkforwin(matrix)
                matrix[x][y] = 0
                if result.win:
                    if result.winnerId == playerId:
                        result.x = x
                        result.y = y
                        return result
    return False

# return True is there are no zeros in the matrix
# False otherwise
def matrixIsFull(matrix):
    fullMatrix = True
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == 0:
                fullMatrix = False
    return fullMatrix

def seeOutcomeForXY(matrix, x, y):
    m = list(matrix)
    m[x][y] = ID_COMPUTER
    
    flag = seeOutcome(m, ID_PLAYER)
    
    m[x][y] = 0
    return flag

# base case: win, loss or tie
# return FLAG_SAFE for tie
# return FLAG_UNSAFE for loss
# return FLAG_WIN to win
# node is cleared (set to safe) if there is a another path on the node that leads to a safe/win flag
def seeOutcome(matrix, currentPlayerId):
    m = matrix
    result = checkForWinningMove(m, currentPlayerId)
    if result:
        if currentPlayerId == ID_PLAYER:
            return FLAG_UNSAFE
        else:
            return FLAG_WIN
    
    if matrixIsFull(m):
        return FLAG_SAFE
    
    if currentPlayerId == ID_PLAYER:
        flag = FLAG_SAFE
        win = True
        for y in range(3):
            for x in range(3):
                if m[x][y] == 0:
                    m[x][y] = ID_PLAYER
                    f = seeOutcome(m, ID_COMPUTER)
                    m[x][y] = 0
                    if f == FLAG_UNSAFE:
                        flag = f
                    if f != FLAG_WIN:
                        win = False
    else:
        flag = FLAG_UNSAFE
        win = False
        for y in range(3):
            for x in range(3):
                if m[x][y] == 0:
                    m[x][y] = ID_COMPUTER
                    f = seeOutcome(m, ID_PLAYER)
                    m[x][y] = 0
                    if f != FLAG_UNSAFE:
                        flag = f
    
    if win:
        flag = FLAG_WIN
    return flag

def checkforwin(matrix):
    result = Result()
    result.win = False
    for id in range(1,3):
        # row win
        for x in range(3):
            win = True
            for y in range(3):
                if matrix[x][y] != id:
                    win = False
                    break;
            if win:
                result.win = True
                result.winnerId = id
                result.winBit = int(math.pow(2,y))
        # column win
        for y in range(3):
            win = True
            for x in range(3):
                if matrix[x][y] != id:
                    win = False
                    break;
            if win:
                result.win = True
                result.winnerId = id
                result.winBit = int(math.pow(2,x+3))
        # diagonal win
        win = True
        for xy in range(3):
            if matrix[xy][xy] != id:
                win = False
                break;
        if win:
            result.win = True
            result.winnerId = id
            result.winBit = int(math.pow(2,6))
        # other diagonal win
        win = True
        for xy in range(3):
            if matrix[xy][2-xy] != id:
                win = False
                break;
        if win:
            result.win = True
            result.winnerId = id
            result.winBit = int(math.pow(2,7))
    
    return result 
    