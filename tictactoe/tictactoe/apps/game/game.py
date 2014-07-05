class InvalidMoveError (Exception):
    pass


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

    def __init__(self, current_game=None):
        if current_game:
            self.winner = current_game['winner']
            self.board = current_game['board']
        else:
            self.winner = None
            self.board = [None for x in range(9)]

    @property
    def available_tiles(self):
        """ Return a list of all tiles that are set to None """
        return [i for i, x in enumerate(self.board) if not x]

    def player_move(self, x):
        """
        Update the the game board when the user plays a tile and check for a winner
        """
        if self.winner or self.board[x]:
            raise InvalidMoveError

        self.board[x] = self.player
        self.winner = self._check_winner()

    def computer_move(self):
        """
        Make the computer perform a valid move and check for a winner
        """
        if not self.winner:
            if len(self.available_tiles) == len(self.board):
                self.board[0] = self.computer  # first move strategy, bypass minimax check
            else:
                value, move = self._minimax(self.computer, 0)
                self.board[move] = self.computer
            self.winner = self._check_winner()

    def _minimax(self, current_player, depth):
        """
        Use the minimax algorithm to determine the next move
        """
        depth += 1
        scores = []
        moves = []
        winner = self._check_winner()

        if winner == self.computer:
            return 10 - depth, None
        elif winner == self.player:
            return depth - 10, None
        elif winner == self.draw:
            return 0, None

        for tile in self.available_tiles:
            self.board[tile] = current_player
            best_score, unused_move = self._minimax(self.player if current_player == self.computer else self.computer, depth)
            scores.append(best_score)
            moves.append(tile)
            self.board[tile] = None

        if current_player == self.computer:
            index = scores.index(max(scores))
        else:
            index = scores.index(min(scores))
        return scores[index], moves[index]

    def _check_winner(self):
        """
        Determine if there is currently a winner by checking each board tile in a combination and seeing if they match
        """
        for combo in self._winning_combos:
            winner = reduce(lambda x, y: x if x == y else None, [self.board[x] for x in combo])
            if winner:
                return winner

        return None if None in self.board else self.draw

    def __unicode__(self):
        return "[TicTacToe winner:{0}, board:{1}".format(self.winner, self.board)

    def __str__(self):
        return unicode(self).encode('utf-8')