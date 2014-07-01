import pdb
import random
import operator


class TicTacToe (object):
    """
    Manages the current game state
    """
    _board_size = 3
    _computer = 'x'
    _player = 'o'
    _draw = '-'

    # winning tile combinations never change, define them on the class level
    _winning_combos = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),    # horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),    # vertical
        (0, 4, 8), (2, 4, 6)                # diagonal
    )

    def __init__(self):
        self.winner = None

        # generate the board with None as the starting values
        self.board = [None for x in range(self._board_size**2)]

        # randomly select starting player
        if random.choice([self._player, self._computer]) == self._computer:
            self.computer_move()

    @property
    def available_tiles(self):
        """ Return a list of all tiles that are set to None """
        return [i for i, x in enumerate(self.board) if not x]

    def check_winner(self):
        """
        Determine if there is currently a winner. Should only be called after a valid move is made.
        """
        winner = reduce(lambda x, y: x or y, [self.board[combo[0]] for combo in self._winning_combos
                                              if all(self.board[combo[0]] == self.board[x] for x in combo)])

        if not winner and not None in self.board:
            return self._draw
        return winner

    def player_move(self, x):
        """
        Update the the game board when the user plays a tile and check for a winner
        """
        if self.board[x]:
            raise Exception('That move has already been taken.')

        self.board[x] = self._player
        self.winner = self.check_winner()
        return self.winner

    def computer_move(self):
        """
        Make the computer perform a valid move and check for a winner
        """
        value, x = self._minimax(self._computer, self.board)
        self.board[x] = self._computer
        self.winner = self.check_winner()
        return self.winner

    def _minimax(self, player, board):
        """
        Use the minimax algorithm to determine the next move
        """
        if self.winner == self._computer:
            return 1, None
        elif self.winner == self._player:
            return -1, None
        elif self.winner == self._draw:
            return 0, None

        if player == self._computer:
            best_value, best_play = float('-inf'), None
            op = operator.gt
            next_player = self._player
        else:
            best_value, best_play = float('inf'), None
            op = operator.lt
            next_player = self._computer

        for x in self.available_tiles:
            board[x] = player
            value, unused_play = self._minimax(next_player, board)

            if op(value, best_value):
                best_value, best_play = value, x

        return best_value, best_play