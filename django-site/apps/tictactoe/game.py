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
    
    # the algorithm works like this:
    #   check each move the computer can take
    #   generate all the possible outcomes that lead up to the player winning
    #   add up all the possible wins for that move
    #   take the move that has the least winnable outcomes for the player
    nextX = 0
    nextY = 0
    max = 0
    first = True
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == 0:
                count = countWinnableOutcomes(matrix, x, y)
                if (count > max) or first:
                    max = count
                    first = False
                    nextX = x
                    nextY = y
    
    result.x = nextX
    result.y = nextY
    
    return result

# entry function to begin recursion
# count up the number of winnable outcomes for the player if the computer chooses [x,y]
def countWinnableOutcomes(matrix, x, y):
    m = list(matrix)
    m[x][y] = ID_COMPUTER
    count = addPossibleLosses(m, 0, ID_PLAYER)
    m[x][y] = 0
    return count

# return the number winnable outcomes for the next turn
# if there are no outcomes for the next turn, then
#   do the same for all possible moves of the turn after next
#   ...and so on...
def addPossibleLosses(matrix, count, playerId):
    numWins = 0
    if playerId == ID_PLAYER:
        for y in range(3):
            for x in range(3):
                if matrix[x][y] == 0:
                    matrix[x][y] = playerId
                    result = checkforwin(matrix)
                    matrix[x][y] = 0
                    if result.win:
                        if result.winnerId == ID_PLAYER:
                            numWins += 1
    
    if numWins > 0:
        return count+numWins
    
    for y in range(3):
        for x in range(3):
            if matrix[x][y] == 0:
                matrix[x][y] = playerId
                nextPlayerId = ID_PLAYER if (playerId == ID_COMPUTER) else ID_COMPUTER
                count = addPossibleLosses(matrix, count, nextPlayerId)
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
    