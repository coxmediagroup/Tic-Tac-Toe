DEFAULT_BOARD_SIZE = 3

class Board(object):
    ''' Simple class which represents a TicTacToe game board.  '''
    OPEN = ' '
    X = 'X'
    O = 'O'

    class InvalidMove(ValueError): pass

    def __init__(self, x_first=True, size=DEFAULT_BOARD_SIZE):
        assert(size > 1)
        self.size = size
        self._state = self.OPEN * (size ** 2)
        self._players = (self.O, self.X) if x_first else (self.X, self.O)
        self._moves = []

    def _mark_position(self, position, marker):
        assert(len(marker) == 1)
        self._state = self._state[:position] + marker + self._state[position + 1:]

    def move(self, position, player):
        ''' Places a move on the board at the provided position.
            position is an integer in the range 0-(board size ** 2)
            player is a boolean indicating the player who went first (True)
            or second (False) '''
        if(self._state[position] != self.OPEN):
            raise self.InvalidMove('That board position has already been played')
        self._mark_position(position, self._players[player])
        self._moves.append((position, player)) # add to the stack

    def undo(self):
        ''' Undo the last move made '''
        position, player = self._moves.pop()
        self._mark_position(position, self.OPEN)

    def open_moves(self):
        ''' Returns a tuple of state indices for board positions that have
            not yet been played.  '''
        s = self._state
        return tuple(i for i in range(len(s)) if s[i] == self.OPEN)

    def winner(self):
        ''' Determines if the board state contains a winning condition.
            Returns the winner (X or O) or None if no win.  '''
        # Not optimized for speed.  If the AI is too slow calculating moves
        # this is probably the first place to look.
        state = self._state
        board_size = self.size
        diag1 = ''
        diag2 = ''
        for i in range(board_size):
            # Check for horizontal win
            s = state[i * board_size:(i + 1) * board_size] # One row
            first = s[0]
            if((first != self.OPEN) and (s.count(first) == len(s))):
                return first
            # Check for vertical win
            s = ''.join(state[(j * board_size) + i] for j in range(board_size))
            first = s[0]
            if((first != self.OPEN) and (s.count(first) == len(s))):
                return first
            # Accumulate diagonals
            diag1 += state[(board_size * i) + i]
            diag2 += state[(board_size * i) + (board_size - i - 1)]

        # Check diagonals
        for s in (diag1, diag2):
            first = s[0]
            if((first != self.OPEN) and (s.count(first) == len(s))):
                return first

        return None

    def draw(self):
        ''' Is this game a draw?  '''
        return not self.OPEN in self._state

    def _board_string(self, state):
        return '-----\n'.join(
            '|'.join(
                state[i * self.size:(i + 1) * self.size]) + '\n' for i in range(self.size))

    def get_layout(self):
        ''' Return a string showing the board layout with available moves
            indicated by the move number for that spot. '''
        state = self._state
        return self._board_string(
            ''.join(
                state[i] if state[i] != self.OPEN else str(i + 1) for i in range(self.size ** 2)))

    def __str__(self):
        return self._board_string(self._state)


