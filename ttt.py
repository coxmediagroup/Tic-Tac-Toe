"""ttt: interactive tac-tac-toe game

"""

import sys

PLAYER_1 = 'X'
PLAYER_2 = 'O'

# Set to true to get debugging output about the tree search.
DEBUG = False
##DEBUG = True

def other_player(player):
    """(str): str

    Given the constant for one player, returns the other one.
    """
    return (PLAYER_1
            if (player == PLAYER_2)
            else PLAYER_2)

class Board:
    """Class representing a game state.

    The cells of the board are numbered like this:
      012
      345
      678

    And will contain 'None' if the cell is empty, 'X', or 'O'.
    """
    def __init__(self):
        self._board = [None] * 9

    def copy(self):
        """(): Board

        Make a copy of this Board instance and return it.
        """
        b = Board()
        b._board = self._board[:]
        return b

    def is_cell_blank(self, cell):
        """(int): bool

        Returns true if the cell is blank.
        """
        assert 0 <= cell < 9
        return (self._board[cell] is None)

    def is_full(self):
        """(): bool

        Returns true if the board is full and no further moves can be made.
        """
        return (None not in self._board)

    def legal_moves(self):
        """(): [int]

        Yields a list of indexes where a move can be made.
        """
        for i in range(9):
            if self.is_cell_blank(i):
                yield i
        
    def record(self, cell, player):
        """(int, str)

        Record a move.
        """
        assert 0 <= cell < 9
        assert player in (PLAYER_1, PLAYER_2)
        self._board[cell] = player

    def output(self, stream=None):
        """(file): None

        Prints out an ASCII representation of the board.  Defaults
        to standard output if no file-like object is supplied.
        """
        if stream is None:
            stream = sys.stdout

        for y in range(3):
            for x in range(3):
                cell = y*3 + x
                value = self._board[cell]
                if value is None:
                    value = str(cell+1)
                stream.write(' ' + value + ' ')
                stream.write('|')
            stream.write('\n')
            stream.write((3*4)*'=' + '\n')

    def get_winner(self):
        """(): str

        If someone has won, returns the PLAYER_1/PLAYER_2 constant of
        that player.

        If no one has won, returns None.
        """
        def generate_indexes():
            """(): [(int, int, int)]

            Internal function that yields 3-tuples containing the cell
            indexes for the rows, columns, diagonals, etc.
            """

            for i in range(3):
                yield (i*3, i*3+1, i*3+2)  # Rows
                yield (i, 3+i, 6+i)        # Columns

            yield (0, 4, 8)                # Diagonal, top left to lower right
            yield (2, 4, 6)                # Diagonal, upper right to lower left

        for indexes in generate_indexes():
            contents = [self._board[i] for i in indexes]
            if contents.count(PLAYER_1) == 3:
                return PLAYER_1
            elif contents.count(PLAYER_2) == 3:
                return PLAYER_2

        return None

    def score(self):
        """(str): int

        Returns the score of the position, from the point of view
        of the specified player.  Player 1 winning is +<very large>,
        and player 2 winning is -<very large>.  Non-winning positions are 0.
        """
        winner = self.get_winner()
        if winner == PLAYER_1:
            return sys.maxint
        elif winner == PLAYER_2:
            return -sys.maxint
        else:
            return 0

    def find_move(self, player):
        """(): int

        Selects a move for the specified player.
        """
        best_move, score = self._minimax(other_player(player), depth=3)
        if best_move is None:
            # Pick an arbitrary cell.
            # XXX should probably take the middle first, then a corner,
            # then pick randomly.
            best_move = self._board.index(None)
        return best_move

    def _minimax(self, player, depth):
        """(str, int): (int, int)

        Do a mini-max search of the game tree, based upon the implementation
        described in http://en.wikipedia.org/wiki/Minimax.  Returns
        the best cell to take, 
        """
        if depth <= 0:
            if DEBUG:
                print 'Depth <= 0; score=', self.score()
                self.output()
            return (None, self.score())
        if self.is_full():
            if DEBUG:
                print 'Board is full; score=', self.score()
                self.output()
            return (None, self.score())

        if player == PLAYER_1:
            best_score = -sys.maxint
        else:
            best_score = sys.maxint
        best_move = None

        for move in self.legal_moves():
            child = self.copy() ; child.record(move, player)
            _, move_score = child._minimax(other_player(player), depth-1)
            if DEBUG:
                print 'Scoring node %i for move %i' % (move_score, move+1)
            if player == PLAYER_1:
                if move_score > best_score:
                    best_score = move_score
                    best_move = move
            else:
                if move_score < best_score:
                    best_score = move_score
                    best_move = move

        return (best_move, best_score)

def main():
    while True:
        print "Would you like the first move? (Y/N)",
        resp = raw_input()
        resp = resp.strip()
        resp = resp.lower()
        if resp.startswith(('y', 'n')):
            break

    if resp.startswith('y'):
        computer_player = PLAYER_2
    else:
        computer_player = PLAYER_1

    board = Board()
    current_player = PLAYER_1
    while not (board.get_winner() or board.is_full()):
        if computer_player == current_player:
            print 'Thinking...'
            cell = board.find_move(current_player)
            print 'Selecting cell', cell+1
            assert board.is_cell_blank(cell)
        else:
            board.output()
            while True:
                print '\nEnter the number of your next square (1-9):',
                cell = raw_input()
                cell = cell.strip()
                # Check for valid cell number.
                if cell not in '123456789':
                    continue
                cell = int(cell) - 1
                if not board.is_cell_blank(cell):
                    print '*** That cell is already occupied.'
                    continue

                break

        # Record the move and switch to the other player.
        board.record(cell, current_player)
        current_player = other_player(current_player)

    winner = board.get_winner()
    if winner == computer_player:
        print 'Yay!  I won!'
    elif winner is not None:
        print 'Congratulations!  You won!'
    else:
        assert board.is_full()
        print 'Draw -- the board is full.'

