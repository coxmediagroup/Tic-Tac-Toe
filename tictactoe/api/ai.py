from collections import defaultdict
from itertools import chain, permutations, combinations
import sys
import random

INFINITY = sys.maxint

WINNING_COMBINATIONS = [
    (0, 1, 2), # row 1
    (3, 4, 5), # row 2
    (6, 7, 8), # row 3
    (0, 3, 6), # column 1
    (1, 4, 7), # column 2
    (2, 5, 8), # column 3
    (0, 4, 8), # diagonal top left to bottom right
    (2, 4, 6), # diagonal top right to bottom left
]

permutation_iters = [permutations(item, 3) for item in WINNING_COMBINATIONS]
WINNING_PERMUTATIONS = set(chain(*permutation_iters))


class TicTacToeNode(object):
    """ Represents a single move on a tic tac toe board.

    parent: previous move
    move: cell this move occupies

    cells:
        0 | 1 | 2
       ---+---+---
        3 | 4 | 5
       ---+---+---
        6 | 7 | 8
    """
    def __init__(self, move=None, parent=None):
        """ Add a new node to an existing tree by supplying the move and the
        parent node.
        """
        self._children = None

        if move is None and parent is not None:
            raise ValueError("Move cannot be None if parent is not None")
        self.parent = parent
        if move is not None:
            move = int(move)
        self.move = move
        self.validate_moves()

    def validate_moves(self):
        valid_cells = set(range(9))
        moves = set(self.moves)
        invalid_moves = moves - valid_cells
        if invalid_moves:
            raise ValueError("Invalid Moves: {0}".format(list(invalid_moves)))

    @classmethod
    def from_history(cls, *moves):
        """ Alternate constructor. Create a tree of tic-tac-toe nodes
        by supplying the history of moves.
        """
        parent = None
        if not moves:
            node = cls()

        for move in moves:
            node = cls(move, parent)
            parent = node

        return node

    def is_win(self, positions):
        """ Check to see if the given positions consitute a win.
        """
        possible_wins = combinations(positions, 3)
        return any((item in WINNING_PERMUTATIONS for item in possible_wins))

    @property
    def terminal(self):
        """ A node is a terminal node if it has no valid children.
        This means all cells have been played or a win exists on the board.
        """
        out_of_moves = len(self.children) == 0
        has_winner = self.is_win(self.p1_moves) or self.is_win(self.p2_moves)
        is_terminal = has_winner or out_of_moves
        return is_terminal

    @property
    def moves(self):
        """ A list of the moves taken to get to this node (inclusive).
        """
        moves = self.parent.moves if self.parent is not None else []
        if self.move is not None:
            moves += [self.move]
        return moves

    @property
    def p1_moves(self):
        """ A list of the moves taken by player one to get to this node.
        """
        return self.moves[::2]

    @property
    def p2_moves(self):
        """ A list of the moves taken by player two to get to this node.
        """
        return self.moves[1::2]

    @property
    def is_max_player(self):
        """ Returns True if this node represents a play by the maxing player
            and False if it represents a play by the min player

            Max player will always play on an odd turn [1,3,5,7,9]
        """
        even_num_moves = len(self.moves) % 2
        return bool(even_num_moves)

    @property
    def children(self):
        all_moves = set(range(9))
        available_moves = all_moves - set(self.moves)
        if self._children is None:
            self._children = [TicTacToeNode(move, self)
                for move in available_moves]
        return self._children

    def __repr__(self):
        return "TicTacToeNode[pos:{0}]".format(self.move)


def score(node):
    """ Heuristic for minimax algorithm.
    Player 1 is max player.
    Player 2 is min player.

    Using depth modification from http://www.neverstopbuilding.com/minimax
    This ensures we try to win as quickly as possible but lose as slowly as
    possible.
    """
    depth = len(node.moves)
    if node.is_win(node.p1_moves):
        return 10 - depth
    if node.is_win(node.p2_moves):
        return -10 + depth
    return 0


# TODO: Speed up with caching or pruning
def minimax(node, depth, max_player):
    """ Implementation of the minimax algorithm.
    More info here: http://en.wikipedia.org/wiki/Minimax
    """
    if depth == 0 or node.terminal:
        return node, score(node)

    if max_player:
        best_value = -INFINITY
        best_nodes = []
        for child in node.children:
            _, val = minimax(child, depth - 1, False)
            if val > best_value:
                best_value = val
                best_nodes = [child]
            if val == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes), best_value
    else:
        best_value = INFINITY
        best_nodes = []
        for child in node.children:
            _, val = minimax(child, depth - 1, True)
            if val < best_value:
                best_value = val
                best_nodes = [child]
            if val == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes), best_value


def get_recommended_play(node):
    """ Use minimax algorithm to get the next recommended play given
    a TicTacToeNode.
    """
    depth = 9 - len(node.moves)
    max_player = not node.is_max_player
    node, _ = minimax(node, depth, max_player)
    return node


def draw_board(node):
    """ Print a representation of the tic tac toe board.
    """
    board = defaultdict(lambda: " ")
    board.update({pos: 'x' for pos in node.p1_moves})
    board.update({pos: 'o' for pos in node.p2_moves})
    print (
        " {0} | {1} | {2}\n"
        "---+---+---\n"
        " {3} | {4} | {5}\n"
        "---+---+---\n"
        " {6} | {7} | {8}\n"
    ).format(*[board[i] for i in range(9)])


if __name__ == "__main__":
    def play(node):
        while not node.terminal:
            draw_board(node)
            node = get_recommended_play(node)
        else:
            draw_board(node)

    node = TicTacToeNode()
    play(node)
