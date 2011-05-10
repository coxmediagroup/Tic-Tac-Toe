from common import Storage, EMPTY, NOUGHT, CROSS, debug, indexes
from random import choice

class Participant(object):
    """ Base class for game participants."""
    def __init__(self):
        self.shape = EMPTY
        self.opponent_shape = EMPTY
    
    def setShape(self, shape):
        """ Set the shape we are using """
        self.opponent_shape = 1 if shape == 2 else 2
        self.shape = shape 
   
    def turn(self, *args):
        """ Override me in subclasses
        returns the move we want to make as (row, column)
        """
        pass
    
    def turnComplete(self, *args):
        """ After we've made our move, draw the board """
        print Storage()._game_board.drawBoard()

class ThreeByThreeLocalHuman(Participant):
    """ Console player for a game """
    def __init__(self):
        pass
        
class Ai(Participant):
    def __init__(self):
        Participant.__init__(self)

    def turn(self, *args):
        next_move = None
        board, vert_list, nw_list, sw_list = Storage()._game_board.winLists()
        for f in (self.checkWinning, self.checkForking, self.randMove):
            next_move = f(Storage()._game_board.board, 
                        vert_list, nw_list, sw_list)
            # print '%s has next_move as %s'% (f.func_name, next_move)
            if next_move: 
                break
        # print 'returning ', next_move
        return next_move
    
    def checkWinning(self, board, v, nw, sw):
        """ Check to see if there are any winning moves
        on the board, priorities is ours, then blocking
        our opponents """
        losses = []
        iterations = -1
        for row in board + v + [nw] + [sw]:
            # print row
            coord = None
            iterations += 1
            row_set = set(row)
            #print "v is",  v
            #print row, row_set, indexes(row, 0)
            if len(row_set) == 2 and 0 in row_set and len(indexes(row, 0)) == 1:
                ## This sucks but whatever
                if row in board and iterations < 3:
                    coord = (iterations,row.index(0))
                elif row in v:
                    coord =  (row.index(0), v.index(row))
                elif row == nw and iterations == 7:
                    coord = (row.index(0), row.index(0))
                elif row == sw and iterations > 7:
                    coord = (row.index(0), (row.index(0) - len(board[0]) -1) * -1)
                if coord:
                    if Storage()._game_board.board[coord[0]][coord[1]]:
                        coord = None
                    elif not self.shape in row:
                        losses.append(coord)
                    else:
                        return coord
        if len(losses):
            return losses[0]
        else:
            return None

    def checkForking(self, board, v, nw, sw):
        """ Check the playing board for possible forks and return the solution
        ai forks are priority, blocking forks after that """
        h           = {1 : [], 2 : [], "sets" : []}
        v_dict      = {1 : [], 2 : [], "sets" : []}
        nw_dict     = {1 : [], 2 : [], "sets" : []}
        sw_dict     = {1 : [], 2 : [], "sets" : []}
        my_forks    = []
        thier_forks = []

        for row in board + v + [nw]  +[sw]:
            row_set = set(row)
            if len(row_set) == 2 and 0 in row_set and len(indexes(row, 0)) == len(row) -1:
                for ind in indexes(row, 0):
                    row_set = list(row_set) #FIXME: dirty boy,, dirty dirty dirty
                    plyr = 1 if 1 in row_set else 2
                    if row in board:
                        h[plyr].append((board.index(row), ind))
                    elif row in v:
                        v_dict[plyr].append((ind, v.index(row)))
                    elif row == nw:
                        nw_dict[plyr].append([[],[]])
                    elif row == sw:
                        sw_dict[plyr].append((ind ,(ind - len(board - 1)) * -1)) 
            
        for dic in [h, v_dict, nw_dict, sw_dict]:
            for i in [1,2]:
                dic["sets"].append(set(dic[i]))
        
        # I don't think I'm scoring points for clarity
        for i in [1,2]:
            if i == self.shape:
                ar = my_forks
            else:
                ar = thier_forks
            ar.append(h["sets"][i -1]       & v_dict["sets"][ i -1])
            ar.append(h["sets"][i -1]       & nw_dict["sets"][i -1])
            ar.append(h["sets"][i -1]       & sw_dict["sets"][i -1])
            ar.append(v_dict["sets"][i -1]  & nw_dict["sets"][i -1])
            ar.append(v_dict["sets"][i -1]  & sw_dict["sets"][i -1])
       
        if len(my_forks):
            return my_forks[0]
        elif len(thier_forks):
            return thier_forks[0]
        else:
            return None

    def randMove(self,board, *args):
        """ Move to any spot on the board that's open, starting with center,
        then corners, then first available"""
        res = None
        center = [(len(board)/2 )]*2
        if board[center[0]][center[1]] == EMPTY:
            # print 'returning center ', center
            res = center
        if not res:
            for i in (0, len(board) - 1):
                for j in (0, len(board) - 1):
                    if board[i][j] == EMPTY:
                        res = (i, j)
        while not res:
            k = choice(range(0, len(board)))
            l = choice(range(0, len(board[0])))
            if board[k][l] == EMPTY:
                res = (k, l)
        return res 
