import random

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
    
    #is there a spot to move?
    fullMatrix = True
    for row in range(3):
        for c in range(3):
            if matrix[row][c] == 0:
                fullMatrix = False
                break;
    
    if fullMatrix:
        return False
    
    #right now just random
    while True:
        x = random.randint(0,2);
        y = random.randint(0,2);
        if matrix[x][y] == 0:
            result.x = x
            result.y = y
            break
    
    return result

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
            if matrix[-xy][-xy] != id:
                win = False
                break;
        if win:
            result.win = True
            result.winnerId = id
    
    return result 
    