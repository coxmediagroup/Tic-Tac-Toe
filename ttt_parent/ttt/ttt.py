import re
import string
from random import randint

# ttt contains the functions needed for running a simple tic-tac-toe game

# This is a regex that checks that the string representing the board is valid.
checker = re.compile('[_xo]{9}')

def isValid(board):
    """
    This function takes a 9-character string and returns true if it's a valid tic-tac-toe board, false otherwise.
    Conditions checked for are:
       -- length.
       -- made up of characters '_', 'x', or 'o' (though having to pop the regex output seems a little ugly).
       -- that the number of 'x' marks is within 0 or 1 of the number of 'o' marks (x goes first in tic-tact toe).
    """
    if len(board)!=9:
        return False;
    board = checker.findall(board).pop()
    if len(board)!=9:
        return False;
    dif = string.count(board, 'x') - string.count(board, 'o')    
    if( (dif < 0) or (dif > 1) ):
        return False
    return True


def boardCondition(board):
    """
    board -- 9 char string of 'x','o' or '_' chars.

    This function evaluates the current condition of a tic-tac-toe board.
    It does not take into account whose turn it is or anything of the sort.
    Likewise, it does not check for a legal board.

    Its design is predicated on the idea that there's no reason to maintain persistant data
    about something as simple as a tic-tac-toe board. Rather, board state and moves
    are classified every time.

    Returns a ridiculous 10-tuple of game state information (it's a little excessive).
    Items:    
        -- blocked (item 0) : array of the 3-item tuples defining winning lines that have been blocked by having an x and an o on them somewhere.
        -- xdoubles (item 1) : array of the 3-item tuples defining winning lines that have two x's in them and no o's
            (in other words, if it's x's turn, they can win if this is not empty, and if it's o's, then they must block.)
        -- odoubles (item 2) : array of the 3-item tuples defining winning lines that have two o's in them and no x's
            (like xdoubles, but with o's).
        -- threat (item 3) : winning lines with no moves along them.
        -- winRow (item 4) : if there's a winning possition (3 in a row), this returns the winning row(s).
        -- winner (item 5) : if there's a winner, is it x or o.
        -- gameOver (item 6) : is the game over.
        -- number of moves (item 7) : how many x's and o's are on the board.
        -- xsingles (item 8) : lines with 1 x and no o's.
        -- osingles (item 9) : lines with 1 o and no x's.
        
    """
    blocked = []
    xsingles = []
    osingles = []
    xdoubles = []
    odoubles = []
    winRow = []
    start = board
    gameOver = False
    winner = ""
    threat = [ (0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6) ] # these are all the possible winning lines in the game
    remove = []
    for i in threat:
        # when called, examines each of the 8 possible winning lines
        a = board[i[0]]
        b = board[i[1]]
        c = board[i[2]]
        row = a + b + c
        xcount = string.count(row, 'x')
        ocount = string.count(row, 'o')
        if ( xcount == 3 ):
            gameOver = True
            winner = 'x'
            winRow.append(i)
        elif ( ocount == 3 ):
            gameOver = True
            winner = 'o'
            winRow.append(i)
        elif ( (ocount > 0) and (xcount > 0) ):
            blocked.append(i)
            remove.append(i)
        elif (xcount == 2):
            xdoubles.append(i)
            remove.append(i)
        elif (ocount == 2):
            odoubles.append(i)
            remove.append(i)
        elif (ocount == 1):
            osingles.append(i)
            remove.append(i)
        elif (xcount == 1):
            xsingles.append(i)
            remove.append(i)
    for i in remove:
        threat.remove(i)
    return ( blocked, xdoubles, odoubles, threat, winRow, winner, gameOver, string.count(board, 'x') + string.count(board, 'o'), xsingles, osingles)


def earlyGame(board, player, condition):
    """
    board -- the same 9-char string we keep passing around
    player -- one char representing whether it's x or o's turn
    condition -- a previously generated 10-tuple representing game state

    returns a 4-tuple:
    -- boolean : True if game is over, False if it's not
    -- winner : empty string, unless winner, then 'x' or 'o'
    -- next move : int representing where the next move is played. -1 if no next move.
    -- player : 1-char string indicating what player plays in the next move slot.
    """
    if(condition[7] == 0):    # if it's the first move
        if (player != 'x'):   # make sure only x moves first
            return (False, '', -1, '')
        else:                 # first move is random
            return (False, '', randint(0,8), 'x')
    if(condition[7] == 1):    # if second move, make sure it's o's turn
        if (player != 'o'):
            return (False, '', -1, '')
        else:                 # if x played in middle, o plays in a corner
            if (board[4] == 'x'):
                return (False, '', (0,2,6,8)[randint(0,3)], 'o')
            else:             # otherwise o plays in middle
                return (False, '', 4, 'o')
    if(condition[7] == 2):    # if computing third move, make sure it's x's turn
        if (player != 'x'):
            return (False, '', -1, '')
        else:
            square = board.index('x')       # get first move spot
            if( (square != 4) and (board[4] == 'o') ): # if o went in center
                for i in condition[8][0]:   # then go somewhere on an xsingles axis
                    if i != square:
                        return (False, '', i, 'x')
            elif(square != 4):
                return (False, '', 4, 'x')  # if o didn't go in center and x hasn't, go in center
            else:   # otherwise go in a corner oposite the axis of corners that o played in
                if((board[0] == 'o') or (board[8] == 'o')):
                    return (False, '', (2,6)[randint(0,1)], 'x')
                elif((board[2] == 'o') or (board[6] == 'o')):
                    return (False, '', (0,8)[randint(0,1)], 'x')
                else:
                    return (False, '', (0,2,6,8)[randint(0,3)], 'x')
    # if(condition[7] == 3):
    #    if (player != 'o'):
            


def plotMove(board, player):
    """
    board -- string of 9 chars made up of x, o, or _. 
    player -- char representing x or o
    
    Takes a board, check that it's valid, then computes the next move for player.
    Will accept a wrong player as the one to make the next move.
    
    Has some GI-GO issues with weird board input that shouldn't come up during a game.
    
    Returns a 4 tuple:
    --  boolean : false if game is not over, true if it is
    --  player : a 1-char string representing the player who will win with the given move
    --  position: where on the board the next move is played
    --  player : which player is playing the next move
    """
    if isValid(board):
        condition = boardCondition(board)
        if(condition[6] == True): # game is already over
            return ( True, condition[5], -1, "" )
        if(condition[7] < 3): # early game needs the early game engine
            return earlyGame(board, player, condition) 
        if(condition[7] == 9): # if there are 9 chars on the board, it's over
            return ( True, condition[5], -1, "" )
        elif (player == 'x'): 
            if( condition[1] != [] ): # if x can win, it does so
                win = condition[1][0]
                if(board[win[0]] == '_'):
                    return (True, 'x', win[0], 'x')
                if(board[win[1]] == '_'):
                    return (True, 'x', win[1], 'x')
                if(board[win[2]] == '_'):
                    return (True, 'x', win[2], 'x')
            if( condition[2] != [] ): # if x must block, it does so
                block = condition[2][0]
                if(board[block[0]] == '_'):
                    return (False, '', block[0], 'x')
                if(board[block[1]] == '_'):
                    return (False, '', block[1], 'x')
                if(board[block[2]] == '_'):
                    return (False, '', block[2], 'x')
            else:
                return (False, '', board.index('_'), 'x') # otherwise, it's safe to choose the first empty space
        elif (player == 'o'):
            if( condition[2] != [] ): # if o can win, it does so
                block = condition[2][0]
                if(board[block[0]] == '_'):
                    return (True, 'o', block[0], 'o')
                if(board[block[1]] == '_'):
                    return (True, 'o', block[1], 'o')
                if(board[block[2]] == '_'):
                    return (True, 'o', block[2], 'o')
            if( condition[1] != [] ):
                win = condition[1][0] # if o must block, it does so
                if(board[win[0]] == '_'):
                    return (False, '', win[0], 'o')
                if(board[win[1]] == '_'):
                    return (False, '', win[1], 'o')
                if(board[win[2]] == '_'):
                    return (False, '', win[2], 'o')
            if( (board[0] == 'x') and (board[8] == 'x') and (condition[7] < 5) ):                    # if blue has split
                return (False, '', (1,3,5,7)[randint(0,3)], 'o')
            if( (board[2] == 'x') and (board[6] == 'x') and (condition[7] < 5) ):
                return (False, '', (1,3,5,7)[randint(0,3)], 'o')
            else:
                return (False, '', board.index('_'), 'o')
                
        return (False, '', -1, '') # these last three returns show up if something's wrong
    else:
        return (False, '', -1, '')
    return (False, '', -1, '')


