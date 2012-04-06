from common import Storage, EMPTY, NOUGHT, CROSS, debug, indexes
from random import choice
import sys

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
        self.displayMsg(Storage()._game_board.drawBoard())

    def displayMsg(self, msg):
        """ Method for displaying text on the users screen """
        print msg

class ThreeByThreeLocalHuman(Participant):
    """ Console player for a game """
    def __init__(self):
        Participant.__init__(self)
        self.displayMsg("Welcome to tic-tac-toe")
        self._buildKeymap()

    def _buildKeymap(self):
        """ Method to build the keymap list attribute
            Not in __init__ as Storage() call corrupts
            subclass initializations.
        """
        self.game_board = Storage()._game_board
        self.board = self.game_board.board
        self.keymap = []
        
        ## Put arrays into the keymap array
        for i in range(0, len(self.board)):
            self.keymap.append([])
        
        ## Assign numbers to the places
        for j in range(0, len(self.board)*len(self.board)):
            self.keymap[j/len(self.board)].append(j+1)

    def turn(self):
        """ Called to start the players turn """
        moved = False
        prompt = "Your turn, enter space to occupy, or \"help\" for help: "
        while not moved:
            inp = raw_input(prompt)
            moved = self.handleInput(inp)
        for row in self.keymap:
            if moved in row:
                return (self.keymap.index(row), row.index(moved))
        moved = False
    
    def handleInput(self, inp):
        commands = ["help", "board"]
        inp = inp.strip()
        try: 
            inp = int(inp)
            if inp in range(1,(len(self.board)*len(self.board)+1)):
                self.displayMsg("\n")
                return inp
            else:
                raise ValueError("Space index out of range")
        except ValueError:
            if hasattr(self, "%s_command" % inp):
                getattr(self, "%s_command" % inp)()
            else:
                self.displayMsg("Sorry, command not recognized\n")
        return False
    
    def help_command(self):
        self.displayMsg("""command list:\n\thelp: This help\n\tboard: show the current board
        exit: Exit the program\n\n board keybindings:\n""")
        
        board_text = ""
        for row in self.keymap:
            first = True
            if not board_text == "":
                board_text += ("-------"*len(self.keymap)) + "\n"
            for item in row:
                if not first:
                    board_text += "|"
                else:
                    first = False
                board_text += "  %s  " % item 
            board_text += "\n"
        self.displayMsg(board_text)

    def board_command(self):
        self.displayMsg(self.game_board.drawBoard())
    
    def exit_command(self):
        sys.exit(0)
    

class Ai(Participant):
    def __init__(self):
        Participant.__init__(self)

    def turn(self, *args):
        next_move = None
        board, vert_list, nw_list, sw_list = Storage()._game_board.winLists()
        for f in (self.checkWinning, self.checkForking, self.randMove):
            next_move = f(Storage()._game_board.board, 
                        vert_list, nw_list, sw_list)
            if next_move: 
                break
        return next_move
    
    def checkWinning(self, board, v, nw, sw):
        """ Check to see if there are any winning moves
        on the board, priorities is ours, then blocking
        our opponents """
        losses = []
        iterations = -1
        for row in board + v + [nw] + [sw]:
            coord = None
            iterations += 1
            row_set = set(row)
            if len(row_set) == 2 and EMPTY in row_set and len(indexes(row, EMPTY)) == 1:
                ## This sucks but whatever
                if row in board and iterations < len(board):
                    coord = (iterations,row.index(0))
                elif row in v and iterations in range(len(board), len(board)*2):
                    coord =  (row.index(0), v.index(row))
                elif row == nw and iterations == len(board) * 2:
                    coord = (row.index(0), row.index(0))
                elif row == sw:
                    coord = (row.index(0), (row.index(0) - (len(board) -1)) * -1)
                if coord:
                    if board[coord[0]][coord[1]]:
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
        # TODO: It would be great to intercept all these loops
        # and test for intersections so we could avoid some overhead
        # but i haven't the time right now to do that. 

        h           = {1 : [], 2 : [], "sets" : {1:[], 2:[]}}
        v_dict      = {1 : [], 2 : [], "sets" : {1:[], 2:[]}}
        nw_dict     = {1 : [], 2 : [], "sets" : {1:[], 2:[]}}
        sw_dict     = {1 : [], 2 : [], "sets" : {1:[], 2:[]}}
        my_forks    = []
        their_forks = []
        iterations = -1
        for row in board + v + [nw]  +[sw]:
            iterations += 1
            row_set = set(row)
            if len(row_set) == 2 and 0 in row_set and len(indexes(row, 0)) == len(row) -1:
                for ind in indexes(row, 0):
                    row_set = list(row_set) #FIXME: dirty boy,, dirty dirty dirty
                    plyr = 1 if 1 in row_set else 2
                    if row in board and iterations < len(board):
                        h[plyr].append((board.index(row), ind))
                    elif row in v and iterations in range(len(board), len(board)*2):
                        v_dict[plyr].append((ind, v.index(row)))
                    elif row == nw and iterations == len(board)*2:
                        nw_dict[plyr].append((ind, ind))
                    elif row == sw:
                        sw_dict[plyr].append((ind ,(ind - len(board) -1) * -1)) 
            
        for dic in [h, v_dict, nw_dict, sw_dict]:
            for i in [1,2]:
                print dic[i]
                dic["sets"][i].append(set(dic[i]))
        
        # I don't think I'm scoring points for clarity
        for i in [1,2]:
            if i == self.shape:
                ar = my_forks
            else:
                ar = their_forks
            ar.append(h["sets"][i][0]       & v_dict["sets"][i][0])
            ar.append(h["sets"][i][0]       & nw_dict["sets"][i][0])
            ar.append(h["sets"][i][0]       & sw_dict["sets"][i][0])
            ar.append(v_dict["sets"][i][0]  & nw_dict["sets"][i][0])
            ar.append(v_dict["sets"][i][0]  & sw_dict["sets"][i][0])
       
        if len(my_forks):
            for i in my_forks:
                return i
        elif len(their_forks):
            for i in their_forks:
                return i
        else:
            return None

    def randMove(self,board, *args):
        """ Move to any spot on the board that's open, starting with center,
        then corners, then first available"""
        res = None
        center = [(len(board)/2 )]*2
        if board[center[0]][center[1]] == EMPTY:
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


