from ttt import *
from participants import *
from common import Storage
from twisted.internet import defer

class TelnetGame(Game):
    """ Game subclass modified to run as part of a twisted server
    """
    def __init__(self, protocol):
        self.protocol = protocol
        Game.__init__(self)
    
    def _initPlayers(self):
        """ Initialize the player instances from storage """
        storage = Storage(self.protocol.identifier)
        self.players = [storage._player_one, storage._player_two]
        self.active_player,self.idle_player = self.randStart()
        self.active_player.setShape(NOUGHT)
        self.idle_player.setShape(CROSS)    

    @defer.inlineCallbacks
    def run(self):
        """ Run method to work with twisted reactor """
        from twisted.internet import reactor
        next_move = yield self.active_player.turn()
        if Storage(self.protocol.identifier)._game_board.place(
                        self.active_player.shape, next_move):
            self.move_count += 1
            self.turnComplete()
        if self.running:
            reactor.callLater(0.1, self.run)
    
    def displayMsg(self, msg):
        """ Output text to player """
        self.protocol.sendData(msg + "\n")

    def checkGameOver(self):
        """ check the board for game over by win states """
        board, v, nw, sw = Storage(
                        self.protocol.identifier)._game_board.winLists()
        for row in board + v + [nw] + [sw]:
            row_set = set(row)
            if len(row_set) == 1 and not 0 in row:
                self.displayMsg(shape_map[row[0]] + " won!")
                self.running = False
                break

class TelnetHuman(ThreeByThreeLocalHuman):
    def __init__(self, protocol):
        self.protocol = protocol
        ThreeByThreeLocalHuman.__init__(self)
        self.d = defer.Deferred()

    def _buildKeymap(self):
        self.game_board = Storage(self.protocol.identifier)._game_board
        self.board = self.game_board.board
        self.keymap = []
        
        ## Put arrays into the keymap array
        for i in range(0, len(self.board)):
            self.keymap.append([])
        
        ## Assign numbers to the places
        for j in range(0, len(self.board)*len(self.board)):
            self.keymap[j/len(self.board)].append(j+1)
    
    def turn(self):
        """ Called to start the players turn,
        @returns: twisted.internet.defer.deferred which will hold
        a valid move postion on user input"""
        self.displayMsg(
                "Your turn, enter space to occupy, or \"help\" for help:")
        return self.d
        
    def dataReceivedHandler(self, data):
        if Storage(
            self.protocol.identifier)._game_instance.active_player == self:
            move = self.handleInput(data)
            if move :
                for row in self.keymap:
                    if move in row:
                        self.d.callback((self.keymap.index(row), 
                                        row.index(move)))
                        self.d = defer.Deferred()
            else:
                self.turn()
        else:
            self.displayMsg("Wait your turn!")

    def turnComplete(self):
        self.displayMsg(self.game_board.drawBoard())

    def displayMsg(self, msg):
        self.protocol.sendData(msg + "\n")

    def board_command(self):
        self.displayMsg(self.game_board.drawBoard())

    def exit_command(self):
        self.protocol.transport.loseConnection()

class TelnetAi(Ai):
    def __init__(self, protocol):
        self.protocol = protocol
        Ai.__init__(self)
    
    def turn(self, *args):
        next_move = None
        board,vert_list,nw_list,sw_list = Storage(
                self.protocol.identifier)._game_board.winLists()
        for f in (self.checkWinning, self.checkForking, self.randMove):
            next_move = f(
                    Storage(self.protocol.identifier)._game_board.board, 
                    vert_list, nw_list, sw_list
                        )
            if next_move: 
                break
        return next_move
    
    def turnComplete(self, *args):
        """ After we've made our move, draw the board """
        self.displayMsg(
                Storage(self.protocol.identifier)._game_board.drawBoard())
    
    def displayMsg(self, msg):
        self.protocol.sendData(msg + "\n")
        
