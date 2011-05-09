class Board():
    """ Game board class that has basic game board utility functions """
    def __init__(self):
        pass


class Game:
    """ Class to control the game logic """
    def __init__(self):
        pass
    
    def run(self):
        """ Cheesy main loop"""
        pass
    
    def turnComplete(self):
        """ Swap the active players, check to see if there was
        a gameover event, and perform any required cleanup """
        pass

    def randStart(self):
        """ Randomly choose who gets to go first """
        pass

    def checkGameOver(self):
        """ Check to see if the game is a draw or someone has won """
        pass

if __name__ == "__main__":
    Storage()._game_board = Board()
    Storage()._player_one = Ai()
    Storage()._player_two = LocalHuman()
    Storage()._game_instance = Game()
    Storage()._game_instance.run()
