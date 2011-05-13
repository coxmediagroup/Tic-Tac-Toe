import random


TOKENS = ['x', 'o']

ROWS = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]]


class random_choice(object):
    """ given a current board, make a random choice of the open squares
    """

    @classmethod
    def choose(cls, current_board, my_symbol='x'):
        open_cells = []
        for idx, cell in enumerate(current_board):
            if cell not in TOKENS:
                open_cells.append(idx)

        if not open_cells:
            # no possible move, return -1
            return -1

        val = random.choice(open_cells)
        return val

    @classmethod
    def is_win(cls, current_board):
        for row in ROWS:
            counts = dict(zip(TOKENS, [0, 0]))
            for cell in row:
                val = current_board[cell]
                if val not in TOKENS:
                    continue
                else:
                    counts[val] += 1
            if 3 in counts.values():
                return True
        return False


OTHERS = {'x': 'o', 'o': 'x'}


class MinMax(object):
    """ compute moves using the minmax alogrithm
    """
    
    board = []
    player = ''
    game_over = False
    _score = None
    
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self._calculate_score()

    def _get_children(self):
        """ return the possible moves available from this board
        """
        for idx, cell in enumerate(self.board):
            if cell not in TOKENS:
                new_board = self.board[:]
                new_board[idx] = self.player
                yield MinMax(new_board, OTHERS[self.player]), idx
                

    def _calculate_line_score(self, line):
        """ calculate the value of one line of a board
        """
        counts = dict(zip(TOKENS, [0,0]))
        for cell in line:
            if cell in TOKENS:
                counts[cell] += 1

        if 3 in counts.values():
            self.game_over = True

        advantage = 1
        if counts['o'] == 0:
            if self.player == 'x':
                advantage = 3
            return (10**counts['x']) * advantage
        elif counts['x'] == 0:
            if self.player == 'o':
                advantage = 3
            return -(10**counts['o']) * advantage
        return 0

    def _calculate_score(self):
        """ calculate the value of a board
        """
        if self._score is None:
            self._score = 0
        for row in ROWS:
            line = [self.board[cell] for cell in row]
            self._score += self._calculate_line_score(line)

    @property
    def score(self):
        """ return the calculated score for this board
        """
        if self._score is None:
            self._calculate_score()
        return self._score

    @property
    def is_terminal(self):
        if self.game_over:
            return True
        for val in self.board:
            if val not in TOKENS:
                return False
        return True

    def choose(self, depth, alpha, beta):
        """ implementation of long-form minmax with alpha-beta pruning
        """
        best_move = -1
        if depth == 0 or self.is_terminal:
            return self.score, best_move

        for child, move in self._get_children():
            score, next_move = child.choose(depth -1, alpha, beta)
            if self.player != 'x':
                if beta > score:
                    beta = score
                    best_move = move
                    if alpha >= beta:
                        break
            else:
                if alpha < score:
                    alpha = score
                    best_move = move
                    if alpha >= beta:
                        break
        
        scores = {'x': alpha, 'o': beta}
        best_score = scores[self.player]
        return best_score, best_move
