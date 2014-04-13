from funcy import all


class Game():
    CELL_STATES = {
        'free': 0,
        'ai': 1,
        'user': 2
    }

    BOARD_SIZE = 3

    def __init__(self):
        self.board = [[self.CELL_STATES['free'] for x in range(self.BOARD_SIZE)] 
                      for y in range(self.BOARD_SIZE)]

    def move(self, x, y):
        if self.board[x][y] != self.CELL_STATES['free']:
            return False
        self.board[x][y] = self.CELL_STATES['user']
        return True

    def is_over(self):
        flattened = chain(*self.board)
        if all(lambda x: x != self.CELL_STATES['free'], flattened):
            return self.NOT_OVER
