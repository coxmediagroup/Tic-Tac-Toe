"""A base implementation for a Tic-Tac-Toe game"""
import random


PLAYER_O = 'circle'
PLAYER_X = 'cross'
PLAYERS = (PLAYER_O, PLAYER_X)


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
        winner = []

        def is_winner(move_0, move_1, move_2):
            """helper for checking matches"""

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

    def get_available_moves(self):
        """Returns a sequence of available moves on the board"""
        available_moves = []

        for column in range(self.size):
            for row in range(self.size):
                move = self.get_move_at_position((column, row))

                if move is None:
                    available_moves.append((column, row))

        return available_moves

    def print_board(self):
        """Prints a human readable representation of the current board state"""

        def get_player_name(player):
            """Returns a human readable version of the player name"""

            if player is None:
                return '_'
            if player is PLAYER_O:
                return 'O'
            return 'X'

        for row in range(self.size):
            print '%s %s %s' % (
                    get_player_name(self.get_move_at_position((0, row))),
                    get_player_name(self.get_move_at_position((1, row))),
                    get_player_name(self.get_move_at_position((2, row))),
                    )


WIN_COMBOS = (
        # columns
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),

        # rows
        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),

        # diagonals
        ((0, 0), (1, 1), (2, 2)),
        ((0, 2), (1, 1), (2, 0)),
    )


class AIPlayer(object):
    """An AI Tic-Tac-Toe player

    Guaranteed to always at least stalemate

    It works by:
        Can it win in one move? Do that.
        Can the opponent win in one move? Block that.

        Otherwise play the optimal opening.

        After that just choose randomly from available moves
    """

    def __init__(self, player):
        self.player = player
        self.opponent = PLAYER_X if self.player == PLAYER_O else PLAYER_O

    def _can_player_win_next_move(self, player, board):
        """Checks for a move the specified player can win with"""

        # find if the player can win in one move
        for win_condition in WIN_COMBOS:
            moves = (board.get_move_at_position(win_condition[0]),
                     board.get_move_at_position(win_condition[1]),
                     board.get_move_at_position(win_condition[2]))

            if None not in moves:
                continue

            if moves.count(player) == 2:
                return win_condition[moves.index(None)]

        return None

    def get_next_move(self, board):
        """Returns the position of the next move"""
        available_moves = board.get_available_moves()

        # can I win in one move?
        move = self._can_player_win_next_move(self.player, board)
        if move is not None:
            return move

        # can the opponent win in one move?
        move = self._can_player_win_next_move(self.opponent, board)
        if move is not None:
            return move

        corners = ((0, 0), (2, 0), (0, 2), (2, 2))
        sides = ((1, 0), (2, 1), (1, 2), (0, 1))
        center = (1, 1)

        # Use any corner as the first move
        if len(available_moves) == 9:
            # play a corner
            return random.choice(corners)

        # find the opponents first move
        if len(available_moves) == 8:
            # Respond to the center with a corner
            if board.get_move_at_position(center) != None:
                return random.choice(corners)

            # Respond to a corner with the center
            for corner in corners:
                if board.get_move_at_position(corner) != None:
                    return center

            # Respond to a side with one of three choices
            for edge in sides:
                if board.get_move_at_position(edge) != None:
                    possible_moves = []

                    # the center
                    possible_moves.append(center)

                    if edge[0] == 1:
                        # An adjacent corner
                        possible_moves.append((0, edge[1]))
                        possible_moves.append((2, edge[1]))

                        # Opposite edge
                        if edge[1] == 0:
                            possible_moves.append((1, 2))
                        else:
                            possible_moves.append((1, 0))
                    else:
                        # An adjacent corner
                        possible_moves.append((edge[0], 0))
                        possible_moves.append((edge[0], 2))

                        # Opposite edge
                        if edge[0] == 0:
                            possible_moves.append((2, 1))
                        else:
                            possible_moves.append((0, 1))

                    return random.choice(possible_moves)

        # other wise follow the priority list
        return random.choice(available_moves)
