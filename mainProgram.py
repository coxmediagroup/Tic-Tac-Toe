import random
from random import choice
import sys

# The constant varibles that stay fairly consistant
winningSets = [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [6, 4, 2]
aiSets = [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [6, 4, 2]
board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
mockBoard = [0, 1, 2, 3, 4, 5, 6, 7, 8]
playerSelections = []
aiSelections = []


#Checks to see if the user won(verifies
def checkwin():
    """
Verifies if winning set is complete
    """
    x = 0
    for i in winningSets:
        for s in aiSelections:
            if s in i:
                x = x + 1
            else:
                x = 0
                continue
        if x == 3:
            print 'You lose'
            sys.exit()
            break
    x = 0
    for i in winningSets:
        for s in playerSelections:
            if s in i:
                x = x + 1
            else:
                x = 0
                continue
        if x == 3:
            print 'You win'
            sys.exit()
            break

def selectSpace():
    '''
    This method is pretty straightfoward. The user just choses a location on the board
    '''
    print board[0], '|', board[1], '|', board[2]
    print '----------'
    print board[3], '|', board[4], '|', board[5]
    print '----------'
    print board[6], '|', board[7], '|', board[8]
    selection = int(raw_input("What space would you like select 0-8: "))
    print selection
    if board[selection] == 'x' or board[selection] == 'o':
        print 'Spot is already taken, please choose another spot'
    else :
        mockBoard.remove(selection)
        board[selection] = 'x'
        playerSelections.append(selection)

def ai():
    # AI is constantly chosing from a more likely win scenario.
    # This win scenario is dertermined by looking thorough the players selections, and comparing it against win sets. 
    LogicMeter = 4
    countLogic = 0
    startChoice = [0, 6, 2, 8]
    random.shuffle(startChoice)
    if 'x' in board or 'o' in board:
        if len(playerSelections) > 1:
            #Rotate thought the aiSets, and remove all the numbers that the player has selected
            for i in aiSets:
                for r in playerSelections:
                    if r in i:
                        i.remove(r)
            # Rotate through aiSets and choose the ones that have most likelyhood of leting the player win. 
            for i in aiSets:
                countLogic = len(i)
                if countLogic < LogicMeter:
                    for c in aiSelections:
                        if c not in i:
                            LogicMeter = countLogic
                            choice = i
            # Chooses a random number from the LogicMeter and uses that as ai selection
            random.shuffle(choice)
            mockBoard.remove(choice[0])
            aiSelections.append(choice[0])
            board[choice[0]] = 'o'
        elif 0 in playerSelections or 6 in playerSelections or 2 in playerSelections or 8 in playerSelections or 4 in aiSelections:
            # Stops from using the corner trick when going first
            print 'entered again'
            mockBoard.remove(4)
            board[4] = 'o'
            aiSelections.append(4)
        elif 4 in playerSelections and playerSelections == 1:
            board[startChoice[0]] = 'o'
            mockBoard.remove[startChoice[0]]
            aiSelections.append(startChoice[0])
    else:
        mockBoard.remove(board[startChoice[0]])
        aiSelections.append(board[startChoice[0]]) 
        board[startChoice[0]] = 'o'
     
    


while True:
    # Actual program
    selectSpace()
    checkwin()
    ai()
    checkwin()
    if len(mockBoard) == 3:
        print board[0], '|', board[1], '|', board[2]
        print '----------'
        print board[3], '|', board[4], '|', board[5]
        print '----------'
        print board[6], '|', board[7], '|', board[8]
        print 'It\'s a tie. No player can win'
        break
            
                    
                
                        
