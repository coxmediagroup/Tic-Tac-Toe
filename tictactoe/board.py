

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
        self.check_move(player, position)
        self.state[position] = player
        self.last_player = player

    def check_move(self, player, position):
        if player not in self.players:
            raise ValueError('Player must be one of %s' % self.players)
        if player == self.last_player:
            raise ValueError("It is not player %s's turn" % player)
        if position not in self.valid_moves:
            raise ValueError('Position %s is not a valid move' % str(position))

    def get_board_for_move(self, player, position):
        self.check_move(player, position)
        state = self.state[:]
        state[position] = player
        return Board(state=state, last_player=player)

    def iter_rows(self):
        for state_indexes in self.row_definitions:
            yield [self.state[x] for x in state_indexes]
