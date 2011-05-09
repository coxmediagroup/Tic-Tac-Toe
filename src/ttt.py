class Board():
    """ Game board class that has basic game board utility functions """
    def __init__(self):
        pass
    
    def winLists(self):
        """ Returns lists in all directions. This
        method should allow the board to be an arbitrary size
        as long as it maintains an odd count, 1:1 row to column ratio
        """
        pass

    def place(self, shape, index_list):
        """ Attempt to place a piece on the board """
        pass

    def drawBoard(self):
        """ Basic draw board function for debugging """
        pass
           
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
        pass
    
    def turnComplete(self):
        """ Swap the active players, check to see if there was
        a gameover event, and perform any required cleanup """
        pass

    def randStart(self):
        """ Randomly choose who gets to go first """
        ap = self.players[choice((0,1))]
        ip = self.players[1] if ap == self.players[0] else self.players[0]
        return (ap, ip)
    
    def checkGameOver(self):
        """ Check to see if the game is a draw or someone has won """
        pass

if __name__ == "__main__":
    Storage()._game_board = Board()
    Storage()._player_one = Ai()
    Storage()._player_two = LocalHuman()
    Storage()._game_instance = Game()
    Storage()._game_instance.run()
