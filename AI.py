
from random import choice

class AI:
    def __init__(self, player, board):
        self.player = player
        self.board = board

    def generateBoards(self):
        return {option:Board(self.board.fetch(), self.board.turn).move(option) for option in self.board.validPositions()}

    def isFirstMove(self):
        if self.board.isEmpty():
            return True
        return False

    # A corner or the center is the best starting move
    def selectFirstMove(self):
        return choice([1, 3, 5, 7, 9])
    
    def isSecondMove(self):
        if len(self.board.validPositions()) == 8:
            return True
        return False

    # If the opponent has taken the center, pick a corner,
    # If the opponent has taken a corner, take the center
    # otherwise pick a corner or the center
    def selectSecondMove(self):
        validMoves = self.board.validPositions()
        if 5 not in validMoves:
            return choice([1, 3, 7, 9])
        if len([position for position in [1, 3, 7, 9] if position not in validMoves()]) != 0:
            return 5
        return choice([1, 3, 5, 7, 9])
        
    def __selectBestMove(self):
        if self.__isFirstMove():
            return self.__selectFirstMove()
        if self.__isSecondMove():
            return self.__selectSecondMove()
        
    def makeMove(self):
        self.board.move(self.__selectBestMove())
