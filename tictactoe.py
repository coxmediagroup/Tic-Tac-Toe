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
        if selection == '1':
            self.human = Human(symbol='X')
            self.computer = Computer(symbol='O')
            self.next_player = self.human
        else:
            self.human = Human(symbol='O')
            self.computer = Computer(symbol='X')
            self.next_player = self.computer

    def toggle_turn(self):
        if self.next_player is self.human:
            self.next_player = self.computer
        else:
            self.next_player = self.human

    def over(self):
        return len(self.board) == self.board.size ** 2

    def run(self):
        print "Game is starting..."
        while not game.over():
            self.next_player.go(self)


class Player(object):
    def __init__(self, symbol=''):
        self.symbol = symbol


class Human(Player):
    def go(self, game):
        print game.board


class Computer(Player):
    def go(self, game):
        pass


class Board(object):
    """Represents current state of game board and provides functional access"""
    def __init__(self, size=3):
        self.size = size
        self.squares = [Square(x, y) for x in range(size) for y in range(size)]

    def __len__(self):
        return len([s for s in self.squares if s.value in ('X', 'O')])

    def __str__(self):
        """
        Print a human-friendly version of the board
        to be shown between turns
        """
        return ''.join("(%d,%d)" % (i.x, i.y) for i in self.squares)


class Square(object):
    """Represents one location on the game board"""
    def __init__(self, x, y, value=' '):
        self.x = x
        self.y = y
        self.value = value

if __name__ == '__main__':
    game = Game()
    game.run()
