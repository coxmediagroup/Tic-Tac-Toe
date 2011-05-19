"""ttt: interactive tac-tac-toe game

"""

import sys

# Constants for the two players
PLAYER_1 = 'X'
PLAYER_2 = 'O'

# Constants for various coordinates on the board.
UL_SQUARE = 0                   # Cell no. for upper left
UP_SQUARE = 1                   # Cell no. for upper middle
UR_SQUARE = 2                   # Cell no. for upper right
LEFT_SQUARE = 3                 # Cell no. for left middle
MIDDLE_SQUARE = 4               # Cell no. for the middle
RIGHT_SQUARE = 5                # Cell no. for right middle
LL_SQUARE = 6                   # Cell no. for lower left
DOWN_SQUARE = 7                 # Cell no. for lower middle
LR_SQUARE = 8                   # Cell no. for lower right

# Dictionary mapping each corner cell no. to the two closest corners.
CORNERS_NEXT = {
    UL_SQUARE: (UR_SQUARE, LL_SQUARE),
    UR_SQUARE: (UL_SQUARE, LR_SQUARE),
    LL_SQUARE: (UL_SQUARE, LR_SQUARE),
    LR_SQUARE: (LL_SQUARE, UR_SQUARE)
}

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

def generate_indexes():
    """(): [(int, int, int)]

    Internal function that yields 3-tuples containing the cell
    indexes for the rows, columns, diagonals, etc.
    """

    for i in range(3):
        yield (i*3, i*3+1, i*3+2)  # Rows
        yield (i, 3+i, 6+i)        # Columns

    # Diagonal, top left to lower right
    yield (UL_SQUARE, MIDDLE_SQUARE, LR_SQUARE)
    # Diagonal, upper right to lower left
    yield (UR_SQUARE, MIDDLE_SQUARE, LL_SQUARE)

# Precompute list of indexes, since it doesn't change over time.
WINNER_INDEXES = list(generate_indexes())

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

    def is_empty(self):
        """(): bool

        Returns true if the board is empty; therefore, this is the first move.
        """
        return (PLAYER_1 not in self._board and PLAYER_2 not in self._board)

    def is_full(self):
        """(): bool

        Returns true if the board is full and no further moves can be made.
        """
        return (None not in self._board)

    def legal_moves(self):
        """(): [int]

        Yields a list of indexes where a move can be made.
        """
        # The  preferred ordering for squares: the middle square, then
        # the corners, then the middle of the sides.  For the corners,
        # we prefer ones with two empty neighbors.
        def preference(cell):
            # The middle square gets the highest score.
            if cell == MIDDLE_SQUARE:
                return 10

            # The middle of the edges get a low score.
            elif cell in (UP_SQUARE, LEFT_SQUARE, RIGHT_SQUARE, DOWN_SQUARE):
                return 0

            # For corners, we'll count
            else:
                c1, c2 = CORNERS_NEXT[cell]
                return (int(self.is_cell_blank(c1)) +
                        int(self.is_cell_blank(c2)))

        cell_list = sorted(range(9), key=preference, reverse=True)
        for i in cell_list:
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
        for indexes in WINNER_INDEXES:
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
        if DEBUG:
            print '\n\n\n' + '='*60

        if self.is_empty():
            # On an empty board, take the middle square.
            best_move = MIDDLE_SQUARE
        else:
            best_move, score = self._minimax(player, depth=3)
            if best_move is None:
                # Pick an arbitrary cell.
                # Probably not invoked, unless _minimax() is buggy or depth
                # was zero.
                best_move = self._board.index(None)
        return best_move

    def _minimax(self, player, depth):
        """(str, int): (int, int)

        Do a mini-max search of the game tree, based upon the implementation
        described in http://en.wikipedia.org/wiki/Minimax.  Returns
        the best cell to take and the resulting score for the node.
        """
        do_score = False
        if depth <= 0:
            do_score = True
            if DEBUG:
                print 'Depth <= 0'

        # No need to search more deeply when someone has won.
        winner = self.get_winner() 
        if winner is not None:
            do_score = True
            if DEBUG:
                print ('Found a winning position for player %s' % winner)
            
        elif self.is_full():
            do_score = True
            if DEBUG:
                print 'Board is full'

        if do_score:
            score = self.score()
            if DEBUG:
                print '\tScore=%i' % score
                self.output()
            return (None, score)

        if player == PLAYER_1:
            best_score = -sys.maxint
        else:
            best_score = sys.maxint
        best_move = None

        for move in self.legal_moves():
            child = self.copy() ; child.record(move, player)
            _, move_score = child._minimax(other_player(player), depth-1)
            if DEBUG:
                print ('Node score = %i for move %i at depth %i' % 
                       (move_score, move+1, depth))
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

