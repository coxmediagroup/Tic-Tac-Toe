def next_move(ttt):
    # get board in 2D array form
    b = ttt.get_board()
    
    # if there's a winning move, take it
    cfw = check_for_win_lose(b)
    if cfw is not None:
        return cfw
    # otherwise, pres on with the next best move
    
    # if 1st move
    if sum(sum(b,[]) == 0:
        return (2,2) # take the center
    
    # if 3rd move, and not a winning one
    if sum(sum(b,[]) == 3:
        if b[0,1]==2 or b[1,2]==2 or b[0,0]==2:
            return (3,3)
        elif b[0,2]==2:
            return (3,1)
        elif b[2,0]==2:
            return (1,3)
        else:#elif b[1,2]==2 or b[2,1]==2 or b[2,2]==2:
            return (1,1)

    # if 5th move, and not a winning or losing one
    



    # if 2nd move
    if sum(sum(b,[])) == 2:
        if b[1,1] == 0:
            return (2,2)
        else:
            return (1,1)

    # if 4th move


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
    return [b[0,ci], b[1,ci], b[2,ci]]

def get_fwd_diag(b):
    return [b[0,2], b[1,1], b[2,0]]

def get_bw_diag(b):
    return [b[0,0], b[1,1], b[2,2]]

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

