from common import Storage, NOUGHT, CROSS, EMPTY, shape_map
from participants import Ai, ThreeByThreeLocalHuman
from random import choice
class Board():
    """ Game board class that has basic game board utility functions """
    def __init__(self, size=3):
        self.board = []
        if size > 0 and size % 2 == 0:
            print "size cannot be an even number, defaulting to 3"
            size = 3
        for i in range(0, size):
            self.board.append([0]*size)
    
    
    
    def winLists(self):
        """ Returns lists in all directions. This
        method should allow the board to be an arbitrary size
        as long as it maintains an odd count, 1:1 row to column ratio 
        """
        vert_set = [[],[],[]]
        nw_set = []
        sw_set = []
        iteration = -1
        for row in self.board:
            iteration += 1
            for i in range(0, len(row)):
                vert_set[i].append(row[i])
            # print "vert set is ", vert_set 
            nw_set.append(row[iteration])
            sw_set.append(row[(iteration - (len(self.board) - 1)) * -1])
        return (self.board, vert_set, nw_set, sw_set)

    def place(self, shape, index_list):
        """ Attempt to place a piece on the board """
        if self.board[index_list[0]][index_list[1]]:
            return False
        else:
            self.board[index_list[0]][index_list[1]] = shape
            return True
    
    def drawBoard(self):
        """ Basic draw board function for debugging """
        board_text = ""
        for row in self.board:
            if not board_text == "":
                board_text += "-----------\n"
            board_text += " %s | %s | %s \n" % (shape_map[row[0]], shape_map[row[1]], shape_map[row[2]]) 
        return board_text

class Game:
    """ Class to control the game logic """
    def __init__(self):
        self.players = [Storage()._player_one, Storage()._player_two]
        self.active_player,self.idle_player = self.randStart()
        self.active_player.setShape(NOUGHT)
        self.idle_player.setShape(CROSS)
        self.move_count = 0
        self.running = True
    
    def run(self):
        """ Cheesy main loop"""
        while self.running :
            next_move = self.active_player.turn()
            if Storage()._game_board.place(self.active_player.shape,next_move):
                self.move_count += 1
                self.turnComplete()

    def turnComplete(self):
        """ Swap the active players, check to see if there was
        a gameover event, and perform any required cleanup """
        ap = self.active_player
        self.active_player = self.idle_player
        self.idle_player = ap
        self.idle_player.turnComplete()
        self.checkGameOver()
    
    def randStart(self):
        """ Randomly choose who gets to go first """
        ap = self.players[choice((0,1))]
        ip = self.players[1] if ap == self.players[0] else self.players[0]
        return (ap, ip)
    
    def checkGameOver(self):
        """ Check to see if the game is a draw or someone has won """
        board, v, nw, sw = Storage()._game_board.winLists()
        for row in board + v + [nw] + [sw]:
            row_set = set(row)
            if len(row_set) == 1 and not 0 in row:
                print shape_map[row[0]], " won!"
                self.running = False
                break
        
        if self.running and self.move_count >= 9:
            print "Draw!"
            self.running = False

if __name__ == "__main__":
    Storage()._game_board = Board()
    Storage()._player_one = Ai()
    Storage()._player_two = Ai() #ThreeByThreeLocalHuman()
    Storage()._game_instance = Game()
    Storage()._game_instance.run()
