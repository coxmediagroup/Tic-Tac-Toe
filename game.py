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
        return all(map(lambda x: x != self.filler, self.flattened))


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

    def move(self, x, y):
        if self.board.get(x, y) != self.CELL_STATES['free']:
            return False
        self.board.set(x, y, self.CELL_STATES['user'])
        self.update_status()
        return True

    def ai_move(self):
        for y in range(self.BOARD_SIZE):
            for x in range(self.BOARD_SIZE):
                if self.board.get(x, y) == self.CELL_STATES['free']:
                    self.board.set(x, y, self.CELL_STATES['ai'])
                    return x, y

    def update_status(self):
        if self.board.is_full():
            self.is_over = True
            self.find_winner()

    def find_winner(self):
        self.message = 'Draw!'
