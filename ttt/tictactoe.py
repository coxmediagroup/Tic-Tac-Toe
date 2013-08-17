"""Play a game of tic-tac-toe
Nick Loadholtes <nick@ironboundsoftware.com
"""

import sys

BOARD = []


def showBoard():
    pass


def getUserInput():
    pass


def checkForWin(board):
    output = False
    #check rows
    for x in range(0, 9, 3):
        print("%s-%s-%s" % (board[x], board[x+1], board[x+2]))
        if board[x] == board[x+1] == board[x+2] and board[x] is not None:
            print("Winner: %s" % board[x])
            return True
            break
    #check cols
    #check diags
    return output


def playGame():
    #Setup board
    #Display start text/rules/etc
    #start loop
    #display board
    #get input
    #check for win
    #make move
    #check for win
    pass

if __name__ == '__main__':
    print("Starting")
    args = sys.argv
    print("args seen:" + str(args))
    playGame()
