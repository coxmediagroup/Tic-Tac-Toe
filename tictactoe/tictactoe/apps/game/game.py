import pdb
import random


class TicTacToe (object):
    """
    Manages the current game state
    """
    _board_size = 3
    _computer = 'x'
    _player = 'o'

    # winning tile combinations never change, define them on the class level
    _winning_combos = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),    # horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),    # vertical
        (0, 4, 8), (2, 4, 6)                # diagonal
    )

    def __init__(self):
        self.winner = None

        # generate the board
        self.board = [None for x in range(self._board_size**2)]

        # randomly select starting player
        if random.choice([self._player, self._computer]) == self._computer:
            self.computer_move()

    @property
    def available_tiles(self):
        """ Return a list of all tiles that are set to None """
        return [x for x in self.board if not x]

    def check_winner(self):
        """
        Determine if there is currently a winner. Should only be called after a valid move is made.
        """
        winner = reduce(lambda x, y: x or y, [self.board[combo[0]] for combo in self._winning_combos
                                              if all(self.board[combo[0]] == self.board[y] for y in combo[1:])])

        if not winner and not self.available_tiles:
            # no winner and no moves left?  it's a cat's game
            pass
        return winner

    def player_move(self, tile):
        """
        Update the the game board when the user plays a tile and check for a winner
        """
        if self.board[tile]:
            # that tile has already been taken
            # TODO: notify the user that they made an illegal move
            return

        self.board[tile] = self._player
        self.winner = self.check_winner()
        return self.winner

    def computer_move(self):
        """
        Make the computer perform a valid move and check for a winner
        """