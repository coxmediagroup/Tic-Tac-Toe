import random, math

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
    
    # first check if there is a winning move
    r = checkForWinningMove(matrix, ID_COMPUTER)
    # if not, check if there is a winning move from the player to block
    if r is False:
        r = checkForWinningMove(matrix, ID_PLAYER)
    if r:
        result.x = r.x
        result.y = r.y
        return result 
    
    # if there are no wins for the next move, then take the path that leads to
    # the outcome with the most winnable vectors (3 across, 3 down, 2 diagonal...so up to 8)
    # the algorithm works like this:
    #   check each move the computer can take
    #   generate all the possible outcomes that lead up to a game over (computer win, player win, cats)
    #   take the move that has the highest number of winnable types (vectors)
    nextX = 0
    nextY = 0
    max = 0
    first = True
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == 0:
                count = countWinnableOutcomesForXY(matrix, x, y)
                if (max > count) or first:
                    first = False
                    max = count
                    nextX = x
                    nextY = y
    
    result.x = nextX
    result.y = nextY
    
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

# entry function to begin recursion
# see how many possible types of wins there are throughout all possible scenarios if the compute chooses [x,y]
# not number of wins, but types (3 across, 3 down, 2 diagonal...so it returns up to 8)
def countWinnableOutcomesForXY(matrix, x, y):
    m = list(matrix)
    m[x][y] = ID_COMPUTER
    bits = countWinnableOutcomes(m, 0, ID_PLAYER, ID_PLAYER)
    m[x][y] = 0
    
    compWins = 0
    
    for i in [1,2,4,8,16,32,64,128]:
        if i & bits:
            compWins += 1

    return compWins

# return the number winnable outcomes types (up to 8 as a bit mask) for the next turn
# if there are no outcomes for the next turn, then
#   do the same for all possible moves of the turn after next
#   ...and so on...
def countWinnableOutcomes(matrix, count, playerId, winnerId):
    gameOver = False
    if playerId == winnerId:
        for y in range(3):
            for x in range(3):
                if matrix[x][y] == 0:
                    matrix[x][y] = playerId
                    result = checkforwin(matrix)
                    matrix[x][y] = 0
                    if result.win:
                        gameOver = True
                        if result.winnerId == winnerId:
                            count = count | result.winBit
    
    if gameOver:
        return count
    
    cats = True
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == 0:
                cats = False
                matrix[x][y] = playerId
                nextPlayerId = ID_PLAYER if (playerId == ID_COMPUTER) else ID_COMPUTER
                count = countWinnableOutcomes(matrix, count, nextPlayerId, winnerId)
                matrix[x][y] = 0
    
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
    