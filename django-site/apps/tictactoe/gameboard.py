import math

class GameBoard:
    
    def __init__(self, rowCount):
        self.rowCount = rowCount
        self.columnCount = rowCount
        self.matrix = [0]*2
        
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
        self.bitIndex = [0]*self.rowCount
        for y in range(self.rowCount):
            self.bitIndex[y] = [0]*self.columnCount
            for x in range(self.columnCount):
                bit = int(math.pow(2, x+y*self.columnCount))
                self.bitIndex[y][x] = bit
    
    def cellToBit(self, cell):
        return self.bitIndex[cell[1]][cell[0]]
    
    def getRowCount(self):
        return self.rowCount
    
    def getColumnCount(self):
        return self.columnCount
    
    def isEmpty(self):
        return True if (self.matrix[0]|self.matrix[1]) == 0 else False
    
    def isFull(self):
        return True if (self.matrix[0]|self.matrix[1]) == 0x1ff else False
    
    def inBounds(self, x, y):
        return True if (x >= 0 and x < self.columnCount and y >= 0 and y < self.rowCount) else False
    
    # pass in a cell (x,y) and return whether or not that
    # space on the board is taken or not
    def isVacant(self, cell):
        x = cell[0]
        y = cell[1]
        if self.inBounds(x,y):
            bit = self.cellToBit(cell)
            m0 = self.matrix[0] & bit
            m1 = self.matrix[1] & bit
            return True if (m0 | m1) == 0 else False
        else:
            return False
    
    def plot(self, cell, xo):
        x = cell[0]
        y = cell[1]
        if self.inBounds(x,y):
            if self.isVacant(cell):
                bit = self.cellToBit(cell)
                self.matrix[xo-1] = self.matrix[xo-1] | bit
                return True
            else:
                return False
        else:
            return False
    
    def clear(self, cell):
        x = cell[0]
        y = cell[1]
        if self.inBounds(x,y):
            bit = self.cellToBit(cell)
            self.matrix[0] = (self.matrix[0] | bit) ^ bit
            self.matrix[1] = (self.matrix[1] | bit) ^ bit
            return True
        else:
            return False
    
    # return a list of (x,y) tuples, each representing an
    # open space on the board
    def getEmptyCells(self):
        cells = []
        for y in range(self.rowCount):
            for x in range(self.columnCount):
                bit = self.cellToBit((x,y))
                if (self.matrix[0]|self.matrix[1]) & bit == 0:
                    cells.append((x,y))
        return cells
    
    # check if the player's (xo) board has matched any defined wins
    def checkForWin(self, xo):
        m = self.matrix[xo-1]
        for win in self.wins:
            if m & win == win:
                return True
        
        return False