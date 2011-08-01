import math

class OutOfBoundsException(Exception): pass
class InvalidMoveException(Exception): pass
class InvalidTypeException(Exception): pass

class GameBoard:
    
    def __init__(self):
        self.boardSize = 3
        
        # two integers for each board
        self.matrix = [0,0]
        
        # default wins (rows, cols, diagonals)
        self.wins = (
            0b111000000,
            0b000111000,
            0b000000111,
            0b100100100,
            0b010010010,
            0b001001001,
            0b100010001,
            0b001010100,
        )
        
        # index x,y points to bit-wise repesentations
        self.bitIndex = [0]*self.boardSize
        for x in range(self.boardSize):
            self.bitIndex[x] = [0]*self.boardSize
            for y in range(self.boardSize):
                bit = int(math.pow(2, x+y*self.boardSize))
                self.bitIndex[x][y] = bit
    
    def getBoardSize(self):
        return self.boardSize
    
    def isEmpty(self):
        return True if (self.matrix[0]|self.matrix[1]) == 0 else False
    
    def isFull(self):
        return True if (self.matrix[0]|self.matrix[1]) == 0x1ff else False
    
    def inBounds(self, cell):
        x = cell[0]
        y = cell[1]
        return True if (x >= 0 and x < self.boardSize and y >= 0 and y < self.boardSize) else False
    
    # pass in a cell (x,y) and return whether or not that
    # space on the board is taken or not
    def isVacant(self, cell):
        x = cell[0]
        y = cell[1]
        if self.inBounds((x,y)):
            bit = self._cellToBit(cell)
            m0 = self.matrix[0] & bit
            m1 = self.matrix[1] & bit
            return True if (m0 | m1) == 0 else False
        else:
            return False
    
    # if the move is valid, mark a spot on the board for the player/turn
    def makeMove(self, cell, turn):
        self._validateMove(cell)
        self._validateTurn(turn)
        
        bit = self._cellToBit(cell)
        self.matrix[turn] = self.matrix[turn] | bit
        
        return True
    
    def clear(self, cell):
        x = cell[0]
        y = cell[1]
        if self.inBounds((x,y)):
            bit = self._cellToBit(cell)
            self.matrix[0] = (self.matrix[0] | bit) ^ bit
            self.matrix[1] = (self.matrix[1] | bit) ^ bit
            return True
        else:
            return False
    
    # return a list of (x,y) tuples, each representing an
    # open space on the board
    def getEmptyCells(self):
        cells = []
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                bit = self._cellToBit((x,y))
                if (self.matrix[0]|self.matrix[1]) & bit == 0:
                    cells.append((x,y))
        return cells
    
    # check if the player's (xo) board has matched any defined wins
    def checkForWin(self, xo):
        m = self.matrix[xo]
        for win in self.wins:
            if m & win == win:
                return True
        
        return False
    
    # convert cell (x,y) to bit
    def _cellToBit(self, cell):
        return self.bitIndex[cell[0]][cell[1]]
    
    # validate that the move is legal
    def _validateMove(self, cell):
        if not isinstance(cell, tuple):
            raise InvalidTypeException('cell must be a 2-tuple')
        
        if not len(cell) == 2:
            raise InvalidTypeException('cell must be a 2-tuple')
        
        if not self.inBounds(cell):
            raise OutOfBoundsException()
        
        if not self.isVacant(cell):
            raise InvalidMoveException('cell '+str(cell)+' is already occupied')

    # validate that the turn (playerId) is valid
    def _validateTurn(self, turn):
        if turn not in range(2):
            raise InvalidMoveException('turn can only be 0 or 1')