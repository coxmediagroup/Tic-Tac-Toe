import random

ID_PLAYER = 1
ID_COMPUTER = 2

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
    
    # choose the next move that has the least amount of possible losses
    # basically, construct a probability matrix where higher numbers represent
    #     a higher possibility of losing for that move
    nextX = 0
    nextY = 0
    min = 0
    first = True
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == 0:
                count = getPossibleLosses(matrix, x, y)
                if (count < min) or first:
                    min = count
                    first = False
                    nextX = x
                    nextY = y
    
    result.x = nextX
    result.y = nextY
    
    return result

# generate a number based on the chance of winning or losing by choosing [x,y]
# higher numbers reveal a better chance of losing
# lower numbers reveal a better chance at winning
def getPossibleLosses(matrix, x, y):
    m = list(matrix)
    m[x][y] = ID_COMPUTER
    count = addPossibleLosses(m, x, y, 0, 1, ID_PLAYER)
    m[x][y] = 0
    return count
    
def addPossibleLosses(matrix, x, y, count, depth, playerId):
    fullMatrix = True
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == 0:
                fullMatrix = False
                matrix[x][y] = playerId
                result = checkforwin(matrix)
                if result.win:
                    matrix[x][y] = 0
                    if result.winnerId == ID_PLAYER:
                        count += 1.0/depth
                else:
                    nextPlayerId = ID_PLAYER if (playerId == ID_COMPUTER) else ID_COMPUTER
                    count = addPossibleLosses(matrix, x, y, count, depth*2, nextPlayerId)
                    matrix[x][y] = 0
    
    if fullMatrix == False:
        return count
    else:
        result = checkforwin(matrix)
        if result.win:
            if(result.winnerId == ID_PLAYER):
                return count+1.0/depth
    return count

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
        # diagonal win
        win = True
        for xy in range(3):
            if matrix[xy][xy] != id:
                win = False
                break;
        if win:
            result.win = True
            result.winnerId = id
        # other diagonal win
        win = True
        for xy in range(3):
            if matrix[xy][2-xy] != id:
                win = False
                break;
        if win:
            result.win = True
            result.winnerId = id
    
    return result 
    