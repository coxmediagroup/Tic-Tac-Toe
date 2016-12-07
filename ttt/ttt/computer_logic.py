import numpy

def next_move(ttt):
    """"This is the primary logic for the unbeatable computer.  a simple
    strategy has been implemented that results in the computer, at
    worst, losing to the oponent, regardless of whether the computer
    makes the first mark or not.
    """
    # get board in 2D array form
    b = ttt.get_board()
    
    # if there's a winning move, take it
    (cfw, win_move) = check_for_win_lose(b)
    if cfw is not None:
        if win_move:
            print 'COMPUTER WINS!'
        return cfw, win_move
    # otherwise, pres on with the next best move

    # get "points" on board.  this tells us not only the move
    # but also who went first
    board_count = sum(sum(b,[]))
    
    # IF COMPUTER HAS FIRST TURN
    # if 1st move
    if board_count == 0:
        return (2,2), False # take the center
        # this is not best strategy for winning, but
        # it the human messes up, the computer can win.
        # taking a corner first makes it a little easier
        # for the computer to win becase the human only
        # has one correct move to make: to take the center
    
    # if 3rd move, and not a winning one
    if board_count == 3:
        if b[0][1]==2 or b[1][0]==2 or b[0][0]==2:
            return (3,3), False
        elif b[0][2]==2:
            return (3,1), False
        elif b[2][0]==2:
            return (1,3), False
        else:#elif b[1][2]==2 or b[2][1]==2 or b[2][2]==2:
            return (1,1), False

    # if 5th move, and not a winning or losing one
    if board_count == 6:
        b5 = numpy.array([[0,2,1],[0,1,0],[2,0,0]])
        if (b == b5).all():
            return (3,3), False
        elif (b == numpy.rot90(b5,1)).all():
            return (3,1), False
        elif (b == numpy.rot90(b5,2)).all():
            return (1,1), False
        elif (b == numpy.rot90(b5,3)).all():
            return (1,3), False

        b5 = numpy.array([[0,0,1],[0,1,2],[2,0,0]])
        if (b == b5).all():
            return (1,1), False
        elif (b == numpy.rot90(b5,1)).all():
            return (1,3), False
        elif (b == numpy.rot90(b5,2)).all():
            return (3,3), False
        elif (b == numpy.rot90(b5,3)).all():
            return (3,1), False

        # at this point, all possible boards should have been covered

    # if 7th move, and a winning or losing one
    if board_count == 9:
        # find the row or col with 2 open slots and mark it
        for ri in range(3):
            r = b[ri]
            if sum([1 if i==0 else 0 for i in r]) == 2:
                if r[0] == 0:
                    return (ri+1,1), False
                else:
                    return (ri+1,2), False
        for ci in range(3):
            c = get_col(b, ci)
            if sum([1 if i==0 else 0 for i in c]) == 2:
                if c[0] == 0:
                    return (1,ci+1), False
                else:
                    return (2,ci+1), False

    
    # IF HUMAN HAS FIRST TURN
    # if 2nd move
    if board_count == 2:
        if b[1][1] == 0:
            # if the center is open, computer has
            # to take it in order to not lose
            return (2,2), False
        else:
            # otherwise take a corner
            return (1,1), False

    # if 4th move
    if board_count == 5:
        # if we took a corner on move 2 and they
        # are using computer's offensive strategy
        # when it is first player
        b4 = [[1,0,0],[0,2,0],[0,0,2]]
        if b==b4:
            return (3,1), False
        # if we took center on move 2
        else:
            b4 = numpy.array([[2,0,0],[0,1,0],[0,0,2]])
            if (b == b4).all() or (b == numpy.rot90(b4,1)).all():
                return (1,2), False

    # overall ELSE -- just find a square
    for ri in range(3):
        for ci in range(3):
            if b[ri][ci] == 0:
                return (ri+1,ci+1), False


def check_for_win_lose(b):
    """Checks for all of the possible win/lose scenarios.  if there is
    a mark which must be made in order to win or in order to avoid
    a loss, then that is the mark the computer must make.
    """
    win_move = None
    block_win = None
    # check for wins based on row
    for ri in range(3):
        row = b[ri]
        if single_move(row):
            if row==[1,1,0]:
                win_move = (ri+1,3)
            elif row==[2,2,0]:
                block_win = (ri+1,3)
            elif row==[1,0,1]:
                win_move = (ri+1,2)
            elif row==[2,0,2]:
                block_win = (ri+1,2)
            elif row==[0,1,1]:
                win_move = (ri+1,1)
            elif row==[0,2,2]:
                block_win = (ri+1,1)
            else:
                print '144 ERROR!'
                print single_move(row)
                print row
                print ' '

    # check for win based on column
    for ci in range(3):
        col = get_col(b,ci)
        if single_move(col):
            if col==[1,1,0]:
                win_move = (3,ci+1)
            elif col==[2,2,0]:
                block_win = (3,ci+1)
            elif col==[1,0,1]:
                win_move = (2,ci+1)
            elif col==[2,0,2]:
                block_win = (2,ci+1)
            elif col==[0,1,1]:
                win_move = (1,ci+1)
            elif col==[0,2,2]:
                block_win = (1,ci+1)
            else:
                print '166 ERROR!'
                print single_move(col)
                print col
                print ' '

    # check for win on backward diagonal
    diag = get_bw_diag(b)
    if single_move(diag):
        if diag==[1,1,0]:
            win_move = (3,3)
        elif diag==[2,2,0]:
            block_win (3,3)
        elif diag == [1,0,1]:
            win_move = (2,2)
        elif diag==[2,0,2]:
            block_win = (2,2)
        elif diag == [0,1,1]:
            win_move = (1,1)
        elif diag==[0,2,2]:
            block_win = (1,1)
    
    # check for win on forward diagonal
    diag = get_fwd_diag(b)
    if single_move(diag):
        if diag == [1,1,0]:
            win_move = (3,1)
        elif diag==[2,2,0]:
            block_win = (3,1)
        elif diag == [1,0,1]:
            win_move = (2,2)
        elif diag==[2,0,2]:
            block_win = (2,2)
        elif diag == [0,1,1]:
            win_move = (1,3)
        elif diag==[0,2,2]:
            block_win = (1,3)

    if win_move is not None:
        return (win_move, True)
    elif block_win is not None:
        return (block_win, False)
    else:
        return (None, False)


def get_col(b, ci):
    """Returns the requested column"""
    return [b[0][ci], b[1][ci], b[2][ci]]


def get_fwd_diag(b):
    """Returns the "forwards" diagnonal triple"""
    return [b[0][2], b[1][1], b[2][0]]


def get_bw_diag(b):
    """Returns the "backwards" diagonal triple"""
    return [b[0][0], b[1][1], b[2][2]]


def single_move(triple):
    """
    function used to determine if a player is a single move away from
    winning base on the provided "triple."  The function calling this
    will determine what cell needs to be marked if a True is returned.
    count number of computer and human marks.
    """
    c = 0 # mark of a 1
    h = 0 # mark of a 2
    for i in triple:
        if i==1:
            c+=1
        elif i==2:
            h+=1
    if (c,h) == (2,0):
        return True
    elif (c,h) == (0,2):
        return True
    return False

