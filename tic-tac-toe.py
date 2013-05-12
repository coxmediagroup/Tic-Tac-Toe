class Game(object):
    """Represents the game, maintains game board and manages game loop"""
    def __init__(self):
        print "Welcome to Tic Tac Toe!"
        self.board = Board()
        self.init_players()

    def init_players(self):
        selection = ''
        prefix = ''
        suffix = '--> Would you like to play first or second? (1 or 2): '
        while selection not in ('1', '2'):
            selection = raw_input('%s%s' % (prefix, suffix))
            prefix = '(Invalid Input) '

    def run(self):
        print "Game is starting..."


class Board(object):
    """Represents current state of game board and provides functional access"""
    def __init__(self, size=3):
        self.size = size
        self.squares = [Square(x, y) for x in range(size) for y in range(size)]

    def __str__(self):
        """
        Print a human-friendly version of the board
        to be shown between turns
        """
        return ''.join("(%d,%d)" % (i.x, i.y) for i in self.squares)


class Square(object):
    """Represents one location on the game board"""
    def __init__(self, x, y, value=''):
        self.x = x
        self.y = y
        self.value = value

if __name__ == '__main__':
    game = Game()
    game.run()
