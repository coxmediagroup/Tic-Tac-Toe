from itertools import product

from funcy import some, all


class Board():
    def __init__(self, size, filler):
        self.size = size
        self.filler = filler
        self.flattened = [filler for x in range(size*size)]

    def set(self, x, y, val):
        self.flattened[y*self.size + x] = val

    def get(self, x, y):
        return self.flattened[y*self.size + x]

    def is_full(self):
        return all(lambda x: x != self.filler, self.flattened)

    def get_crossed_lines(self, x, y):
        yield {(x, y): self.get(x, y) for x in range(self.size)}
        yield {(x, y): self.get(x, y) for y in range(self.size)}
        if x == y:
            yield {(x, y): self.get(x, y) for x, y in zip(range(self.size), range(self.size))}
        if x + y == self.size - 1:
            yield {(x, y): self.get(x, y) for x, y in zip(range(self.size), 
                                                          reversed(range(self.size)))}

    def from_flattened(self, idx):
        return idx % self.size, idx // self.size

    def get_cells_containing(self, mark):
        return [self.from_flattened(idx) for idx, m in enumerate(self.flattened) if m == mark]

    def get_corner_cells(self):
        return product((0, self.size - 1), repeat=2)

    def get_center_cell(self):
        return self.size // 2, self.size // 2

    def get_oposite_cell(self, x, y):
        return self.size - x - 1, self.size - y - 1


class Game():
    CELL_STATES = {
        'free': 0,
        'ai': 1,
        'user': 2
    }

    BOARD_SIZE = 3

    def __init__(self):
        self.board = Board(self.BOARD_SIZE, self.CELL_STATES['free'])
        self.is_over = False
        self.win_lines = []

    def move(self, x, y):
        if self.board.get(x, y) != self.CELL_STATES['free']:
            return False
        self.board.set(x, y, self.CELL_STATES['user'])
        self.update_status(x, y)
        return True

    def is_line_winning(self, line):
        marks_set = set(line.values())
        return len(marks_set) == 1 and marks_set.pop() != self.CELL_STATES['free']

    def ai_try_win(self, free_cells):
        for x, y in free_cells:
            for line in self.board.get_crossed_lines(x, y):
                line[x, y] = self.CELL_STATES['ai']
                if self.is_line_winning(line):
                    return x, y

    def ai_try_block(self, free_cells):
        for x, y in free_cells:
            for line in self.board.get_crossed_lines(x, y):
                line[x, y] = self.CELL_STATES['user']
                if self.is_line_winning(line):
                    return x, y

    def ai_play_center(self, free_cells):
        center_cell = self.board.get_center_cell()
        if center_cell in free_cells:
            return center_cell

    def ai_play_corner(self, free_cells):
        free_corners = [c for c in self.board.get_corner_cells() if c in free_cells]
        if free_corners:
            for corner in free_corners:
                if self.board.get(*self.board.get_oposite_cell(*corner)) == self.CELL_STATES['user']:
                    return corner
            return free_corners[0]


    def ai_stupid_move(self, free_cells):
        return free_cells[0]

    def ai_move(self):
        free_cells = self.board.get_cells_containing(self.CELL_STATES['free'])
        ai_moves = [self.ai_try_win, self.ai_try_block, self.ai_play_center, 
                    self.ai_play_corner, self.ai_stupid_move]
        x, y = some(map(lambda f: f(free_cells), ai_moves))
        self.board.set(x, y, self.CELL_STATES['ai'])
        self.update_status(x, y)
        return x, y

    def update_status(self, x, y):
        self.check_win_state(x, y)
        self.check_fullness()

    def check_win_state(self, x, y):
        for line in self.board.get_crossed_lines(x, y):
            if self.is_line_winning(line):
                self.is_over = True
                if self.board.get(x, y) == self.CELL_STATES['ai']:
                    self.message = 'You lose!'
                else: 
                    self.message = 'You win!'
                self.win_lines.append(line.keys())

    def check_fullness(self):
        if not self.is_over and self.board.is_full():
            self.is_over = True
            self.message = 'Draw!'