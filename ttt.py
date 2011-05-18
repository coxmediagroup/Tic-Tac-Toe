"""ttt: interactive tac-tac-toe game

"""

import sys

PLAYER_1 = 'X'
PLAYER_2 = 'O'

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

    def find_move(self, player):
        """(): int

        Selects a move for the specified player.
        """
        return self._board.index(None)

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
            print 'Selecting cell', cell
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
        current_player = (PLAYER_1
                          if (current_player == PLAYER_2)
                          else PLAYER_2)
    winner = board.get_winner()
    if winner == computer_player:
        print 'Yay!  I won!'
    elif winner is not None:
        print 'Congratulations!  You won!'
    else:
        assert board.is_full()
        print 'Draw -- the board is full.'

