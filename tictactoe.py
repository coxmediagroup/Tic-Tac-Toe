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
        game.toggle_turn()
        move_loc = ''

        print game.board
        print('Where would you like to move?')

        err = ''
        while move_loc not in game.board.unused():
            print err
            move_loc = self.move_prompt(game)
            err = '\nInvalid Selection. Try again.\n'
        move_loc.mark = self.symbol

    def move_prompt(self, game):
        x = ''
        y = ''
        prefix = ''
        while x not in ('0', '1', '2'):
            x = raw_input('%s--> Select an X coordinate: ' % prefix)
            prefix = '(Invalid Input) '
        prefix = ''
        while y not in ('0', '1', '2'):
            y = raw_input('%s--> Select a Y coordinate: ' % prefix)
            prefix = '(Invalid Input) '
        x, y = int(x), int(y)
        return game.board.square(x, y)


class Computer(Player):
    def go(self, game):
        game.toggle_turn()
        game.board.unused()[0].mark = self.symbol


class Board(object):
    """Represents current state of game board and provides functional access"""
    def __init__(self, size=3):
        self.size = size
        self.squares = [Square(x, y) for x in range(size) for y in range(size)]

    def square(self, x, y):
        return [i for i in self.squares if i.x == x and i.y == y].pop()

    def unused(self):
        return [i for i in self.squares if i.mark not in ('X', 'O')]

    def __len__(self):
        return len([s for s in self.squares if s.mark in ('X', 'O')])

    def __str__(self):
        """
        Print a human-friendly version of the board
        to be shown between turns
        """
        res = ['\n    0   1   2\n']
        res.append(' 0  %s | %s | %s\n' %
                   (self.square(0, 0), self.square(1, 0), self.square(2, 0)))
        res.append('   ---+---+---\n')
        res.append(' 1  %s | %s | %s\n' %
                   (self.square(0, 1), self.square(1, 1), self.square(2, 1)))
        res.append('   ---+---+---\n')
        res.append(' 2  %s | %s | %s\n' %
                   (self.square(0, 2), self.square(1, 2), self.square(2, 2)))

        return ''.join(res)


class Square(object):
    """Represents one location on the game board"""
    def __init__(self, x, y, mark=' '):
        self.x = x
        self.y = y
        self.mark = mark

    def __str__(self):
        return self.mark

if __name__ == '__main__':
    game = Game()
    game.run()
