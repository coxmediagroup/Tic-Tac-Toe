"""ttt: interactive tac-tac-toe game

"""

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

    def record(self, cell, player):
        """(int, str)

        Record a move.
        """
        assert 0 <= cell < 9
        assert player in (PLAYER_1, PLAYER_2)
        self._board[cell] = player

    def output(self):
        """Prints out an ASCII representation of the board."""
        
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
    while not board.get_winner():
        if computer_player == current_player:
            print 'Thinking...'
            cell = board.find_move(current_player)
            print 'Selecting cell', cell
            board.record(cell, current_player)
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
    else:
        print 'Congratulations!  You won!'
