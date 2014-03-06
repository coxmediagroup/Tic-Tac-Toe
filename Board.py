
class Board:
    def __init__(self, layout = None, turn = 'X'):
        if layout == None or self.isInvalidBoard(layout):
            layout = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        if turn != 'X' and turn != 'O':
            turn = 'X'
        self.layout = layout
        self.turn = turn

    def isInvalidBoard(self, board):
        valid = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'X', 'O']
        invalidPositions = [position for row in board for position in row if position not in valid]
        if len(invalidPositions) > 0:
            return True
        return False

    def fetch(self):
        return [[column for column in row] for row in self.layout]

    def validPositions(self):
        return [position for row in self.layout for position in row if position != 'X' and position != 'O']

    def isEmpty(self):
        return len(self.validPositions()) == 9

    def isFull(self):
        return len(self.validPositions()) == 0

    # Debug function, not the final view
    def dump(self):
        for row in self.layout:
            for column in row:
                print column, " ",
            print "\n"

    def __getRowColumn(self, position):
        try:
            pos = int(position)
            if pos < 1 or pos > 9:
                return None
            return (int(pos - 1) / 3, (pos - 1) % 3)
        except ValueError:
            return None

    def isValidMove(self, position):
        return position in self.validPositions()

    def changeTurn(self):
        self.turn = 'O' if self.turn == 'X' else 'X'

    def move(self, position):
        if self.isValidMove(position):
            (row, column) = self.__getRowColumn(position)
            self.layout[row][column] = self.turn
            self.changeTurn()
        return self
