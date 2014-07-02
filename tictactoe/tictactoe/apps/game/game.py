import pdb
import operator


class TicTacToe (object):
    """
    Manages the current game state
    """
    # winning tile combinations never change, define them at the class level
    _winning_combos = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),    # horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),    # vertical
        (0, 4, 8), (2, 4, 6)                # diagonal
    )

    computer = 'x'
    player = 'o'
    draw = '-'

    def __init__(self, user_starts=True, session_data=None):
        if session_data:
            self.winner = session_data['winner']
            self.board = session_data['board']
            self.next_turn = session_data['next_turn']
        else:
            self.winner = None
            self.board = [None for x in range(9)]
            self.next_turn = self.player if user_starts else self.computer

        if not user_starts or self.next_turn == self.computer:
            self.computer_move()

    @property
    def available_tiles(self):
        """ Return a list of all tiles that are set to None """
        return [i for i, x in enumerate(self.board) if not x]

    def player_move(self, x):
        """
        Update the the game board when the user plays a tile and check for a winner
        """
        if self.board[x]:
            raise Exception('That move has already been taken.')

        self.board[x] = self.player
        self.winner = self._check_winner()
        self.next_turn = self.computer

    def computer_move(self):
        """
        Make the computer perform a valid move and check for a winner
        """
        value, x = self._minimax(self.computer)

        if x:
            self.board[x] = self.computer
        self.winner = self._check_winner()
        self.next_turn = self.player

    def _check_winner(self):
        """
        Determine if there is currently a winner by checking each board tile in a combination and seeing if they match
        """
        for combo in self._winning_combos:
            winner = reduce(lambda x, y: x if x == y else None, [self.board[x] for x in combo])
            if winner:
                return winner

        return None if None in self.board else self.draw

    def _minimax(self, player):
        """
        Use the minimax algorithm to determine the next move
        """
        winner = self._check_winner()

        if winner == self.computer:
            return 1, None
        elif winner == self.player:
            return -1, None
        elif winner == self.draw:
            return 0, None

        if player == self.computer:
            best_value, best_play = float('-inf'), None
            op = operator.gt
            next_player = self.player
        else:
            best_value, best_play = float('inf'), None
            op = operator.lt
            next_player = self.computer

        for x in self.available_tiles:
            self.board[x] = player
            value, unused_play = self._minimax(next_player)
            self.board[x] = None

            if op(value, best_value):
                best_value, best_play = value, x
        return best_value, best_play