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
        board = Storage()._game_board.board
        self.keymap = []
        
        ## Put arrays into the keymap array
        for i in range(0, len(board)):
            self.keymap.append([])
        
        ## Assign numbers to the places
        for j in range(0, len(board)*len(board)):
            self.keymap[j/len(board)].append(j+1)

    def turn(self):
        """ Called to start the players turn """
        board = Storage()._game_board.board
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
        board = Storage()._game_board.board
        commands = ["help", "board"]
        inp = inp.strip()
        try: 
            inp = int(inp)
            if inp in range(1,(len(board)*len(board)+1)):
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
        self.displayMsg(Storage()._game_board.drawBoard())
    
    def exit_command(self):
        sys.exit(0)
    
class TelnetHuman(ThreeByThreeLocalHuman):
    def __init__(self, protocol):
        self.protocol = protocol
        ThreeByThreeLocalHuman.__init__(self)
    
    def _buildKeymap(self):
        board = Storage(self.protocol.identifier)._game_board.board
        self.keymap = []
        
        ## Put arrays into the keymap array
        for i in range(0, len(board)):
            self.keymap.append([])
        
        ## Assign numbers to the places
        for j in range(0, len(board)*len(board)):
            self.keymap[j/len(board)].append(j+1)
    def turn(self):
        """ Called to start the players turn """
        self.displayMsg("Your turn, enter space to occupy, or \"help\" for help:")

    def dataReceivedHandler(self, data):
        if Storage(self.protocol.identifier)._game_instance.active_player == self:
            move = self.handleInput(data)
            if move :
                pass
            else:
                self.turn()
        else:
            self.displayMsg("Wait your turn!")

    def turnComplete(self):
        self.diplayMsg(Storage(self.protocol.identifier).game_board.drawBoard())

    def displayMsg(self, msg):
        self.protocol.sendData(msg)
    
    def exit_command(self):
        self.protocol.transport.loseConnection()

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
                if row in board and iterations < 3:
                    coord = (iterations,row.index(0))
                elif row in v:
                    coord =  (row.index(0), v.index(row))
                elif row == nw and iterations == 7:
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

        h           = {1 : [], 2 : [], "sets" : []}
        v_dict      = {1 : [], 2 : [], "sets" : []}
        nw_dict     = {1 : [], 2 : [], "sets" : []}
        sw_dict     = {1 : [], 2 : [], "sets" : []}
        my_forks    = []
        their_forks = []

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
                ar = their_forks
            ar.append(h["sets"][i -1]       & v_dict["sets"][ i -1])
            ar.append(h["sets"][i -1]       & nw_dict["sets"][i -1])
            ar.append(h["sets"][i -1]       & sw_dict["sets"][i -1])
            ar.append(v_dict["sets"][i -1]  & nw_dict["sets"][i -1])
            ar.append(v_dict["sets"][i -1]  & sw_dict["sets"][i -1])
       
        if len(my_forks):
            for i in my_forks:
                for j in i:
                    return j
        elif len(their_forks):
            for i in their_forks:
                for j in i:
                    return j
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

class TelnetAi(Ai):
    def __init__(self, protocol):
        self.protocol = protocol
        Ai.__init__(self)
    
    def turn(self, *args):
        next_move = None
        board, vert_list, nw_list, sw_list = Storage(self.protocol.identifier)._game_board.winLists()
        for f in (self.checkWinning, self.checkForking, self.randMove):
            next_move = f(Storage(self.protocol.identifier)._game_board.board, 
                        vert_list, nw_list, sw_list)
            if next_move: 
                break
        return next_move
