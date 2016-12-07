"""A base implementation for a Tic-Tac-Toe game"""
import random
import copy


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

    def _find_player_wins_next_move(self, player, board):
        """Returns all moves that would result in a win for the specified player
        """

        winning_moves = []

        # find if the player can win in one move
        for win_condition in WIN_COMBOS:
            moves = (board.get_move_at_position(win_condition[0]),
                     board.get_move_at_position(win_condition[1]),
                     board.get_move_at_position(win_condition[2]))

            if None not in moves:
                continue

            if moves.count(player) == 2:
                winning_moves.append(
                        (win_condition[moves.index(None)], win_condition))

        return winning_moves

    def _find_fork_for_player(self, player, board, available_moves):
        """Finds a move for the specified player that would
        result in 2 possible ways to win next turn
        """
        #TODO: Ugly and brute force but it works
        for move in available_moves:
            temp_board = copy.deepcopy(board)

            temp_board.add_move(move, player)

            winning_moves = self._find_player_wins_next_move(player, temp_board)

            # found a fork, return it
            if len(winning_moves) > 1:
                return move

        return None

    def _get_corners_adjacent_to_edge(self, edge):
        """Return both corners adjacent to the specified edge"""
        if edge[0] == 1:
            return [(0, edge[1]), (2, edge[1])]
        else:
            return [(edge[0], 0), (edge[0], 2)]

    def _get_opposite_edge(self, edge):
        """Return the edge opposite of the specified edge"""
        if edge[0] == 1:
            return (1, 2 if edge[1] == 0 else 0)
        else:
            return (2 if edge[0] == 0 else 0, 1)

    def _get_opposite_corner(self, corner):
        """Return the corner opposite of the specified corner"""
        if corner[0] == corner[1]:
            if corner[0] == 0:
                return (2, 2)
            else:
                return (0, 0)
        else:
            if corner[0] == 0:
                return (2, 0)
            else:
                return (0, 2)

    def get_next_move(self, board):
        """Returns the position of the next move"""
        available_moves = set(board.get_available_moves())

        # can I win in one move?
        moves = self._find_player_wins_next_move(self.player, board)
        if moves:
            return random.choice(moves)[0]

        # can the opponent win in one move?
        moves = self._find_player_wins_next_move(self.opponent, board)
        if moves:
            return random.choice(moves)[0]

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

                    # adjacent corners
                    possible_moves.extend(
                            self._get_corners_adjacent_to_edge(edge))

                    # opposite edge
                    possible_moves.append(self._get_opposite_edge(edge))

                    return random.choice(possible_moves)

        # Special Cases
        if len(available_moves) == 6:
            # If the opponent has two corners,
            # the logic below would have us play a corner
            # That would allow the opponent to create an unavoidable fork though
            # Instead play an edge
            corner_moves = [board.get_move_at_position(x) for x in corners]

            if corner_moves.count(self.opponent) > 1:
                return random.choice(sides)

            # Fork detection breaks here so hard code it
            center_move = board.get_move_at_position(center)

            if self.player in corner_moves and \
                    self.opponent in corner_moves \
                    and self.opponent == center_move:
                return random.choice(
                        list(available_moves.intersection(corners)))

        # Can I create a fork for myself?
        my_fork = self._find_fork_for_player(
                self.player, board, available_moves)

        if my_fork:
            return my_fork

        # Can the opponent create a fork next turn?
        opponent_fork = self._find_fork_for_player(
                self.opponent, board, available_moves)

        if opponent_fork:
            return opponent_fork

        # if the center is available, play it
        if (1, 1) in available_moves:
            return (1, 1)

        corners_available = available_moves.intersection(corners)

        # if a corner is available,
        # play it only if the opponent is in the opposite corner
        for corner in corners_available:
            opposite_corner = self._get_opposite_corner(corner)

            if self.opponent == board.get_move_at_position(opposite_corner):
                return corner

        # otherwise, play a corner if I can
        if corners_available:
            return random.choice(list(corners_available))

        # other wise play one of the edges
        return random.choice(list(available_moves))
