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
    for x in xrange(0, 9, 3):
        print("%s-%s-%s" % (board[x], board[x+1], board[x+2]))
        if board[x] == board[x+1] == board[x+2] and board[x] is not None:
            print("Winner (row): %s" % board[x])
            return True
            break
    #check cols
    for x in xrange(0, 3):
        print("%s\n%s\n%s" % (board[x], board[x+3], board[x+6]))
        if board[x] == board[x+3] == board[x+6] and board[x] is not None:
            print("Winner (column): %s" % board[x])
            return True
            break
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
