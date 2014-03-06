
class AI:
    def __init__(self, player, board):
        self.player = player
        self.board = board

    def generateBoards(self):
        return {option:Board(self.board.fetch(), self.board.turn).move(option) for option in self.board.validPositions()}

