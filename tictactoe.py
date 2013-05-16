class Game(object):

    """A tic tac toe game.
    Represents the game, maintains game board, two players
    and manages game loop along with who should play next.
    """

    def __init__(self):
        """Create the game board and determine play order."""
        print "Welcome to Tic Tac Toe!"
        self.board = Board()
        self.init_players()

    def init_players(self):
        """Query the user about turn order and create Players appropriately.
        The first player is always represented by X regardless if the first
        player is human or computer. Likewise with player 2, represented by O.
        """
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
        """Swap next_player to mark who should play next
        (not who is playing currently). This must be called
        by Player and its subclasses as the first step in a turn.
        """
        if self.next_player is self.human:
            self.next_player = self.computer
        else:
            self.next_player = self.human

    def over(self):
        """Determine if the game is over, by checking if the board is full
        or if a player has achieved a win scenario.
        """
        #TODO: Yeah, this checks full board but not win scenario yet...
        return len(self.board) == self.board.size ** 2

    def run(self):
        """Start taking turns. This assumes that the board and players
        have been appropriately setup in __init__.
        """
        print "Game is starting..."
        while not game.over():
            self.next_player.go(self)


class Player(object):

    """A base class for Human and Computer player classes."""

    def __init__(self, symbol=''):
        """Store the symbol ('X' or 'O') for the Player."""
        self.symbol = symbol


class Human(Player):

    """Represents data and functionality for human players.
    Handles data input and validation for user interaction.
    """

    def go(self, game):

        """Take a turn. Ask the user for input, keep asking until
        the user chooses one that is untaken then mark that square.
        """

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
        """Ask a user for (X,Y) coordinates that are valid, (i.e. on the
        board) then get that square from the game board and return.
        """
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

    """Represents the computer player in tic tac toe.
    Stores data pertinent to this player and contains logic for move selection.
    """

    def go(self, game):
        """Determine the best possible next move based on current
        board conditions.
        """
        #TODO: sooo, this just grabs the first open square it can right now...
        game.toggle_turn()
        game.board.unused()[0].mark = self.symbol


class Board(object):

    """Represents the current state of the game's board
    and provides functional access.
    """

    def __init__(self, size=3):
        """Create a Square for each open space on a 3x3 grid."""
        self.size = size
        self.squares = [Square(x, y) for x in range(size) for y in range(size)]

    def square(self, x, y):
        """Retrieve a Square given an (X,Y) coordinate pair."""
        return [i for i in self.squares if i.x == x and i.y == y].pop()

    def unused(self):
        """Return a list containing all unclaimed Squares."""
        return [i for i in self.squares if i.mark not in ('X', 'O')]

    def __len__(self):
        """Calculate the number of claimed Squares on the Board."""
        return len([s for s in self.squares if s.mark in ('X', 'O')])

    def __str__(self):
        """Print a human-friendly version of the Board
        to be shown between turns.
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

    """Represents one location on the game board, its location and mark."""

    def __init__(self, x, y, mark=' '):
        """Store coordinates and mark for this Square."""
        self.x = x
        self.y = y
        self.mark = mark

    def __str__(self):
        """Print the mark for this Square ('X','O' or ' ')."""
        return self.mark

if __name__ == '__main__':
    game = Game()
    game.run()
