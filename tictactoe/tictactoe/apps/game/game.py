
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
    def __init__(self):
        pass