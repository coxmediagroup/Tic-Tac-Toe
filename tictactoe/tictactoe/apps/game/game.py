import random


class GameTile ():
    """
    Manages the current game tile at the specified x, y position on the board.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = None


class GameBoard ():
    """
    Manages the current game state
    """
    _BOARD_SIZE = 3
    _COMPUTER = 'x'
    _PLAYER = 'o'

    def __init__(self):
        # generate the tileset
        self.tiles = [[GameTile(x, y) for y in range(GameBoard._BOARD_SIZE)] for x in range(GameBoard._BOARD_SIZE)]

        # determine starting player and play if the computer starts
        if random.choice([GameBoard._PLAYER, GameBoard._COMPUTER]) == GameBoard._COMPUTER:
            # TODO: call the function to trigger computer move
            pass