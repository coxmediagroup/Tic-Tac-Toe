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

    def ai_stupid_move(self, free_cells):
        return free_cells[0]

    def ai_move(self):
        free_cells = self.board.get_cells_containing(self.CELL_STATES['free'])
        print(free_cells)
        x, y = some(map(lambda f: f(free_cells), [self.ai_try_win, self.ai_stupid_move]))
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