"""Play a game of tic-tac-toe
Nick Loadholtes <nick@ironboundsoftware.com
"""

import sys


def _showValue(v, pos):
    "Displays a pretty board so the user knows where to place their marker"
    return v[pos] if v[pos] is not None else pos


def showBoard(board):
    b = board
    for x in xrange(0, 9, 3):
        print("%s-%s-%s" % (_showValue(b, x), _showValue(b, x+1), _showValue(b, x+2)))


def getUserInput():
    print("Where would you like place your O?")
    


def checkForWin(board):
    output = False
    #check rows
    for x in xrange(0, 9, 3):
        print("%s-%s-%s" % (board[x], board[x+1], board[x+2]))
        if board[x] == board[x+1] == board[x+2] and board[x] is not None:
            print("Winner (row %s): %s" % (x, board[x]))
            return True
            break
    #check cols
    for x in xrange(0, 3):
        print("%s\n%s\n%s" % (board[x], board[x+3], board[x+6]))
        if board[x] == board[x+3] == board[x+6] and board[x] is not None:
            print("Winner (column %s): %s" % (x, board[x]))
            return True
            break
    #check diags
    #TODO: Might be a better way to do this check
    if board[0] == board[4] == board[8] and board[x] is not None:
        print("Winner (diagonal 1): %s" % board[0])
        return True
    if board[2] == board[4] == board[6] and board[x] is not None:
        print("Winner (diagonal 1): %s" % board[0])
        return True
    return output


def playGame():
    #Setup board
    board = [None for x in range(9)]
    #Display start text/rules/etc
    print("""\n\nWelcome to this little tic-tac-toe game. I (the computer) will play as X. \
You can play as O. Just enter the number of the cell where you want to place your marker. \
(Enter q if you want to give up and quit.)\n\n""")
    #start loop
    #display board
    showBoard(board)
    #get input
    getUserInput()
    #check for win
    #make move
    #check for win
    pass

if __name__ == '__main__':
    print("Starting")
    args = sys.argv
    # print("args seen:" + str(args))
    playGame()
