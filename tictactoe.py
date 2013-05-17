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
        return self.board.unused() == []

    def run(self):
        """Start taking turns. This assumes that the board and players
        have been appropriately setup in __init__.
        """
        print "Game is starting..."
        while not self.over():
            self.next_player.go(self)


class Player(object):

    """A base class for Human and Computer player classes."""

    def __init__(self, symbol=''):
        """Store the symbol ('X' or 'O') for the Player and opponent."""
        self.symbol = symbol
        self.opponent_symbol = 'O' if self.symbol == 'X' else 'X'


class Human(Player):

    """Represents data and functionality for human players.
    Handles data input and validation for user interaction.
    """

    def go(self, game):

        """Take a turn. Ask the user for input, keep asking until
        the user chooses one that is untaken then mark that square.
        """

        game.toggle_turn()
        move_loc = None

        print game.board
        print('Where would you like to move?')

        err = ''
        while move_loc not in game.board.unused():
            print err
            x, y = self.move_prompt(game)
            move_loc = game.board.square(x, y)
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
        return (int(x), int(y))


class Computer(Player):

    """Represents the computer player in tic tac toe.
    Stores data pertinent to this player and contains logic for move selection.
    """

    def go(self, game):
        """Determine the best possible next move based on current board
        conditions. This algorithm will choose the first possible of the
        following possibilities:

        1) If there is a winning move available (2 marks in a line with the
            third space in the same line available), take it.
        2) If the opponent will have a winning move available on their next
            turn, take the space that would give your opponent the win.
        3) Create a fork if possible. (Where a fork is the condition that
            you have two unbroken lines of two, simultaneously creating two
            possible win conditions on your next move.)
        4) Can you prevent your opponent from creating a fork on their next
            move? This can be accomplished by first possible of the following:
            - Creating a possible win scenario on your next move, forcing
                your opponent to block such that their act of blocking will
                not create a fork for them.
            - Choose the space where the opponent would need to play in order
                to create the fork.
        5) Choose the center space.
        6) Choose an empty corner opposite and diagonal from a corner already
            claimed by the opponent.
        7) Choose any empty corner space.
        8) Choose any empty side space (non-corner edge).

        If the first possible of these steps is always chosen, optimal play
        will result in a win or draw for the computer every time.

        Attribution: http://wikipedia.org/wiki/Tic-tac-toe#Strategy
        Note: Although it is actually optimal for the computer to choose the
        center as the first move (if able) which creates more possibilities
        for a forced win by X, this progam follows the above algorithm stictly
        which still results in a draw in optimal play by O and a win in
        suboptimal play by O. The expectations for the program are that the
        computer will 'never lose'. This holds but the algorithm could
        certainly be improved to win a greater number of times or to do so in
        a faster or more efficient manner.
        """

        #TODO: sooo, this just grabs the first open square it can right now...
        game.toggle_turn()

        win = game.board.winning_moves(self.symbol)
        if win:
            return

        block = game.board.winning_moves(self.opponent_symbol)
        if block:
            return

        fork = game.board.fork_available(self.symbol)
        if fork:
            return

        game.board.unused()[0].mark = self.symbol


class Board(object):

    """Represents the current state of the game's board
    and provides functional access.
    """

    __size = 3
    __indices = (0, 1, 2)

    def __init__(self):
        """Create a Square for each open space on a 3x3 grid."""
        self.squares = [Square(x, y)
                        for x in range(self.__size)
                        for y in range(self.__size)]

    def square(self, x, y):
        """Retrieve a Square given an (X,Y) coordinate pair."""
        return [i for i in self.squares if i.x == x and i.y == y].pop()

    def used(self):
        """Return a list of all squares that have already been claimed"""
        return [i for i in self.squares if i not in self.unused()]

    def unused(self):
        """Return a list containing all unclaimed Squares."""
        return [i for i in self.squares if i.empty()]

    def winning_moves(self, symbol=''):

        """Return a list of all moves which will result in a win for player
        represented by symbol. Return an empty list if none exist.
        """

        res = []

        cols = [[s for s in self.squares if s.x == i and s.mark == symbol]
                for i in range(3)]
        for i, col in enumerate(cols):
            if len(col) == 2:
                j = (set(self.__indices) - set(s.y for s in col)).pop()
                sq = self.square(i, j)
                if sq in self.unused():
                    res.append(sq)

        rows = [[s for s in self.squares if s.y == i and s.mark == symbol]
                for i in range(3)]
        for i, row in enumerate(rows):
            if len(row) == 2:
                j = (set(self.__indices) - set(s.x for s in row)).pop()
                sq = self.square(j, i)
                if sq in self.unused():
                    res.append(sq)

        tl_diag = [s for s in self.squares if s.x == s.y and s.mark == symbol]
        if len(tl_diag) == 2:
            i = (set(self.__indices) - set(s.x for s in tl_diag)).pop()
            sq = self.square(i, i)
            if sq in self.unused():
                res.append(sq)

        tr_diag_ind = tuple((2 - x, x) for x in range(3))
        tr_diag = [s for s in self.squares if
                   (s.x, s.y) in tr_diag_ind and s.mark == symbol]
        if len(tr_diag) == 2:
            i, j = (set(tr_diag_ind) - set((s.x, s.y) for s in tr_diag)).pop()
            sq = self.square(i, j)
            if sq in self.unused():
                res.append(sq)

        return res

    def fork_available(self, symbol=''):
        """Return a list of all moves which will result in creating a fork
        for player represented by symbol. Fork here is determined as the
        existance of two separate, simultaneous threats to win. Return an
        empty list if none exist.
        """
        #TODO
        return []

    def __str__(self):
        """Print a human-friendly version of the Board
        to be shown between turns.
        """
        res = ['\n    0   1   2\n']

        sub = [' %d  %s | %s | %s\n' %
               ((j,) + tuple(self.square(i, j)
               for i in range(3))) for j in range(3)]
        res.append('   ---+---+---\n'.join(sub))

        return ''.join(res)


class Square(object):

    """Represents one location on the game board, its location and mark."""

    def __init__(self, x, y, mark=' '):
        """Store coordinates and mark for this Square."""
        self.x = x
        self.y = y
        self.mark = mark

    def empty(self):
        """Return a bool representing if this square has not been claimed"""
        return self.mark == ' '

    def __str__(self):
        """Print the mark for this Square ('X','O' or ' ')."""
        return self.mark

if __name__ == '__main__':
    game = Game()
    game.run()
