import random


TOKENS = ['x', 'o']

ROWS = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]]


class random_choice(object):
    """ given a current board, make a random choice of the open squares
    """

    @classmethod
    def choose(cls, current_board):
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
