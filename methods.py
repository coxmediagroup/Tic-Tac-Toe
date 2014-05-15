import random
from random import choice
from mainProgram import *

def checkwin():
    """
Verifies if winning set is complete
    """
    x = 0
    for i in winningSets2:
        for s in aiSelections:
            if s in i:
                x = x + 1
            else:
                x = 0
                continue
        if x == 3:
            print 'You lose'
            break
    for i in winningSets2:
        for s in playerSelections:
            if s in i:
                x = x + 1
            else:
                x = 0
                continue
        if x == 3:
            print 'You win'
            break



def selectSpace():
        """


        """
        print board[0], '|', board[1], '|', board[2]
        print '----------'
        print board[3], '|', board[4], '|', board[5]
        print '----------'
        print board[6], '|', board[7], '|', board[8]
        selection = (int(raw_input("What space would you like select 1-9: ")) - 1)
        if board[selection] == 'x' or board[selection] == 'o':
            print 'Spot is already taken, please choose another spot'
        else :
            board2.remove(board[selection])
            board[selection] = 'x'
            playerSelections.append(selection)
            for i in winningSets:
                i.remove(selection)


def ai():
#AI thinks in combinations of 15 (if the player's total has the potential of equaling 15, he'll counter;
# However, the AI will try to reach 15 first as long as he's not at risk.
# The board for the AI looks as such:
# 8(0), 1(1) ,6(2)
# 3(3), 5(4), 7(5)
# 4(6), 9(7), 2(8)
# All possible ways of winning always equals 15
    startChoice = [0, 6, 2, 8]
    random.shuffle(startChoice)
    closestWinner = 4
    if 'x' in board or 'o' in board:
        if 0 in playerSelections or 6 in playerSelections or 2 in playerSelections or 8 in playerSelections and 4 not in playerSelections:
            board2.pop(4)
            board[4] = 'o'
            aiSelections.append(board[4])
        else:
            countPlayer = len(playerSelections)
            if countPlayer == 1:
                for i in winningSets:
                    for s in playerSelections:
                        if s in i:
                            i.remove(s)
                            aiChoice = int(choice(i))
                            print aiChoice
                            for position, item in enumerate(board):
                                if item == aiChoice:
                                    board2.pop(position)
                                    aiSelections.append(board[position])
                                    board[position] = 'o'
                                    continue
                                    
            if countPlayer > 1:
                for i in winningSets:
                    for s in playerSelections:
                        if s in i:
                            i.remove(s)
                for r in winningSets:
                    if len(r) < closestWinner:
                        closestWinner = len(r)
                        bestChance = r
                aiChoice2 = int(choice(bestChance))
                for position, item in enumerate(board):
                    if item == aiChoice2:
                        board2.pop(position)
                        aiSelections.append(board[position])
                        board[position] = 'o'
                




    else:
        board2.remove(board[startChoice[0]])
        board[startChoice[0]] = 'o'
        aiSelections.append(board[startChoice[0]])
