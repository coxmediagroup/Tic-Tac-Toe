import numpy

def next_move(ttt):
    # get board in 2D array form
    b = ttt.get_board()
    
    # if there's a winning move, take it
    cfw = check_for_win_lose(b)
    if cfw is not None:
        return cfw
    # otherwise, pres on with the next best move
    
    # IF COMPUTER HAS FIRST TURN
    # if 1st move
    if sum(sum(b,[]) == 0:
        return (2,2) # take the center
        # this is not best strategy for winning, but
        # it the human messes up, the computer can win.
        # taking a corner first makes it a little easier
        # for the computer to win becase the human only
        # has one correct move to make: to take the center
    
    # if 3rd move, and not a winning one
    if sum(sum(b,[]) == 3:
        if b[0][1]==2 or b[1][0]==2 or b[0][0]==2:
            return (3,3)
        elif b[0][2]==2:
            return (3,1)
        elif b[2][0]==2:
            return (1,3)
        else:#elif b[1][2]==2 or b[2][1]==2 or b[2][2]==2:
            return (1,1)

    # if 5th move, and not a winning or losing one
    if sum(sum(b,[])) == 6:
        b5 = numpy.array([[0,2,1],[0,1,0],[2,0,0]])
        if (b == b5).all():
            return (3,3)
        elif (b == numpy.rot90(b5,1)).all():
            return (3,1)
        elif (b == numpy.rot90(b5,2)).all():
            return (1,1)
        elif (b == numpy.rot90(b5,3)).all():
            return (1,3)

        b5 = numpy.array([[0,0,1],[0,1,2],[2,0,0]])
        if (b == b5).all():
            return (1,1)
        elif (b == numpy.rot90(b5,1)).all():
            return (1,3)
        elif (b == numpy.rot90(b5,2)).all():
            return (3,3)
        elif (b == numpy.rot90(b5,3)).all():
            return (3,1)

        # at this point, all possible boards should have been covered

    # if 7th move, and a winning or losing one
    if sum(sum(b,[])) == 9:
        # find the row or col with 2 open slots and mark it
        for ri in range(3):
            r = b[ri]
            if sum([1 if i==0 else 0 for i in r]) == 2:
                if r[0] == 0:
                    return (ri+1,1)
                else:
                    return (ri+1,2)
        for ci in range(3):
            c = get_col(b, ci)
            if sum([1 if i==0 else 0 for i in c]) == 2:
                if c[0] == 0:
                    return (1,ci+1)
                else:
                    return (2,ci+1)

    # if 9th move, we are at a TIE, just find a square
    # if sum(sum(b,[])) == 12:
    #     for ri in range(3):
    #         for ci in range(3):
    #             if b[ri][ci] == 0:
    #                 return (ri+1,ci+1)

    # IF HUMAN HAS FIRST TURN
    # if 2nd move
    if sum(sum(b,[])) == 2:
        if b[1][1] == 0:
            # if the center is open, computer has
            # to take it in order to not lose
            return (2,2)
        else:
            # otherwise take a corner
            return (1,1)

    # if 4th move
    if sum(sum(b,[])) == 5:
        # if we took a corner on move 2 and they
        # are using computer's offensive strategy
        # when it is first player
        b4 = [[1,0,0],[0,2,0],[0,0,2]]
        if b==b4:
            return (3,1)
        # if we took center on move 2
        else:
            b4 = numpy.array([[2,0,0],[0,1,0],[0,0,2]])
            if (b == b4).all() or (b == numpy.rot90(b4,1)).all():
                return (1,2)

    # overall ELSE -- just find a square
    if sum(sum(b,[])) == 12:
        for ri in range(3):
            for ci in range(3):
                if b[ri][ci] == 0:
                    return (ri+1,ci+1)



def check_for_win_lose(b):
    # check for wins based on row
    for ri in range(3):
        row = b[ri]
        if single_move(row):
            if row == [1,1,0]:
                return (ri+1,3)
            elif row == [1,0,1]:
                return (ri+1,2)
            elif row == [0,1,1]:
                return (ri+1,1)
            else:
                print 'ERROR!'

    # check for win based on column
    for ci in range(3):
        col = get_col(b,ci)
        if single_move(col):
            if col == [1,1,0]:
                return (3,ci+1)
            elif col == [1,0,1]:
                return (2,ci+1)
            elif col == [0,1,1]:
                return (1,ci+1)
            else:
                print 'ERROR!'

    # check for win on backward diagonal
    diag = get_bw_diag(b)
    if single_move(diag):
        if diag == [1,1,0]:
            return (3,3)
        elif diag == [1,0,1]:
            return (2,2)
        elif diag == [0,1,1]:
            return (1,1)
    
    # check for win on forward diagonal
    diag = get_fwd_diag(b)
    if single_move(diag):
        if diag == [1,1,0]:
            return (3,1)
        elif diag == [1,0,1]:
            return (2,2)
        elif diag == [0,1,1]:
            return (1,3)

    # if nothing above caught the return, then there is
    # no win yet
    return None    


def get_col(b, ci):
    return [b[0][ci], b[1][ci], b[2][ci]]

def get_fwd_diag(b):
    return [b[0][2], b[1][1], b[2][0]]

def get_bw_diag(b):
    return [b[0][0], b[1][1], b[2][2]]

def single_move(triple):
    # function used to determine if a player is a
    # single move away from winning.
    # count number of computer and human marks.
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

