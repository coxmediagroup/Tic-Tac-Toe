from ttt import *

"""
The item in this file provide a basic 'test' of tic-tac-toe functionality.
It's not a proper test because rather than have test cases, it just has the 
next move finder find each next move. Some of the moves are random, so about
all you can do is just run pcVpc and see if the game makes sense.

I mean to add some test cases at some point.
"""

def printBoard(board):
    print "%s" % (board[0:3])
    print "%s" % (board[3:6])
    print "%s" % (board[6:9])
    print ""

def pcVpc():
    print 'PC vs CPU'
    board = '_________'
    
    player = ('x', 'o')
    for i in range(0,9):
        print "Turn %d (%s):" % (i, player[i%2])
        g = plotMove(board, player[i%2])
        board = board[:g[2]] + g[3] + board[g[2]+1:]
        printBoard(board)


