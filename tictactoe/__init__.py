"""A base implementation for a Tic-Tac-Toe game"""


PLAYER_O = 'circle'
PLAYER_X = 'cross'


class MoveNotAvailable(Exception):
    """Thrown when trying to make a move on a tile that was already played on"""
    pass


class InvalidPlayerError(Exception):
    """Thrown when making a move to player other than PLAYER_O or PLAYER_X"""
    pass


class Board(object):
    """The Tic-Tac-Toe board"""

    def __init__(self):
        self.board = [
                [None, None, None],
                [None, None, None],
                [None, None, None],
            ]

        self.size = 3

    def get_winner(self):
        """Returns true if a player has won"""

        # To hold the winner for the helper
        winner = [ ]

        # helper for checking matches
        def is_winner(move_0, move_1, move_2):
            # if any haven't been played on, no
            if None in (move_0, move_1, move_2):
                return None

            # if the don't match, no
            if move_0 != move_1 or move_1 != move_2:
                return None

            # winner
            winner.append(move_0)
            return move_0
        
        for idx in range(self.size):
            # check column
            move_0 = self.get_move_at_position((idx, 0))
            move_1 = self.get_move_at_position((idx, 1))
            move_2 = self.get_move_at_position((idx, 2))

            if is_winner(move_0, move_1, move_2):
                return winner[0]

            # check row
            move_0 = self.get_move_at_position((0, idx))
            move_1 = self.get_move_at_position((1, idx))
            move_2 = self.get_move_at_position((2, idx))

            if is_winner(move_0, move_1, move_2):
                return winner[0]

        # all columns and rows checked, check diagonals  
        move_0 = self.get_move_at_position((0, 0))
        move_1 = self.get_move_at_position((1, 1))
        move_2 = self.get_move_at_position((2, 2))

        if is_winner(move_0, move_1, move_2):
            return winner[0]

        move_0 = self.get_move_at_position((0, 2))
        move_1 = self.get_move_at_position((1, 1))
        move_2 = self.get_move_at_position((2, 0))

        if is_winner(move_0, move_1, move_2):
            return winner[0]

        # no winner found
        return None

    def get_move_at_position(self, pos):
        """Returns the move at the specified position"""

        if pos[0] >= self.size or pos[1] >= self.size:
            raise IndexError()

        return self.board[pos[0]][pos[1]]

    def add_move(self, pos, player):
        """Adds a move to the board at position `pos` by player `player`"""

        current_move_at_pos = self.get_move_at_position(pos)

        if current_move_at_pos is not None:
            raise MoveNotAvailable()

        if player not in (PLAYER_X, PLAYER_O):
            raise InvalidPlayerError()

        self.board[pos[0]][pos[1]] = player


class AIPlayer(object):
    """An AI Tic-Tac-Toe player

    Guaranteed to always at least stalemate
    """

    def __init__(self, player):
        pass

    def get_next_move(self, board):
        """Returns the position of the next move"""
        pass
