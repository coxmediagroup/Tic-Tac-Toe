

__all__ = ['Board']


class Board(object):
    """This class defines a 3x3 tic-tac-toe board."""

    x = 'x'

    o = 'o'

    players = [x, o]

    empty = ' '

    row_definitions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],        # Vertical
        [0, 3, 6], [1, 4, 7], [2, 5, 8],        # Horizontal
        [0, 4, 8], [2, 4, 6],                   # Diagonal
        ]

    board_template = """
%s | %s | %s
---------
%s | %s | %s
---------
%s | %s | %s
""".strip()

    @classmethod
    def get_opponent(cls, player):
        """Retrieve the opponent of the given player.

        """
        return {cls.x: cls.o, cls.o: cls.x}[player]

    def __init__(self, state=None, last_player=None):
        if not state:
            state = [self.empty] * 9
        self.state = state
        if not last_player:
            last_player = self.empty
        self.last_player = last_player

    @property
    def printable_state(self):
        return self.board_template % tuple(self.state)

    @property
    def valid_moves(self):
        return [x for x, y in enumerate(self.state) if y == self.empty]

    def add_move(self, player, position):
        """Add a move to the board for the given player and position.
        If the given position is not a valid move, an exception will
        be raised.

        """
        self.check_move(player, position)
        self.state[position] = player
        self.last_player = player

    def check_move(self, player, position):
        """Check that the given move is valid, raising an exception
        for any problem.

        """
        if player not in self.players:
            raise ValueError('Player must be one of %s' % self.players)
        if player == self.last_player:
            raise ValueError("It is not player %s's turn" % player)
        if position not in self.valid_moves:
            raise ValueError('Position %s is not a valid move' % str(position))

    def get_board_for_move(self, player, position):
        """Retrieve a new board with the given move added.

        """
        self.check_move(player, position)
        state = self.state[:]
        state[position] = player
        return Board(state=state, last_player=player)

    def get_winner(self):
        """Retrieve the name of the winning player if there is one, or
        None otherwise.

        """
        for row in self.iter_rows():
            is_winning_row = (row[0] != self.empty and
                              row == [row[0]] * len(row))
            if is_winning_row:
                return row[0]

    def is_game_over(self):
        """Indicate whether the game has been won or lacks valid moves.

        """
        return self.get_winner() or not self.valid_moves

    def iter_rows(self):
        """Iterate over the rows (vertical, horizontal and diagonal)
        in the state matrix.

        """
        for state_indexes in self.row_definitions:
            yield [self.state[x] for x in state_indexes]
