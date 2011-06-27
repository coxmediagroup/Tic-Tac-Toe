class GameBoard:
    
    X = 1
    O = 2
    EMPTY_CELL = 0
    
    def __init__(self, rowCount):
        self.rowCount = rowCount
        self.columnCount = rowCount
        self.matrix = [self.EMPTY_CELL]*rowCount
        for y in range(rowCount):
            self.matrix[y] = [self.EMPTY_CELL]*rowCount
    
    def getRowCount(self):
        return self.rowCount
    
    def getColumnCount(self):
        return self.columnCount
    
    def isEmpty(self):
        for y in range(self.rowCount):
            for x in range(self.columnCount):
                if self.matrix[x][y] != self.EMPTY_CELL:
                    return False
        return True
    
    def isFull(self):
        for y in range(self.rowCount):
            for x in range(self.columnCount):
                if self.matrix[x][y] == self.EMPTY_CELL:
                    return False
        return True
    
    def getXY(self, cell):
        x = cell[0]
        y = cell[1]
        inBounds = True if (x >= 0 and x < self.columnCount and y >= 0 and y < self.rowCount) else False
        if inBounds:
            return self.matrix[x][y]
        else:
            return False
    
    def plot(self, cell, xo):
        x = cell[0]
        y = cell[1]
        inBounds = True if (x >= 0 and x < self.columnCount and y >= 0 and y < self.rowCount) else False
        if inBounds:
            self.matrix[x][y] = xo
            return True
        else:
            return False
    
    def clear(self, cell):
        x = cell[0]
        y = cell[1]
        inBounds = True if (x >= 0 and x < self.columnCount and y >= 0 and y < self.rowCount) else False
        if inBounds:
            self.matrix[x][y] = self.EMPTY_CELL
            return True
        else:
            return False
    
    def getEmptyCells(self):
        cells = []
        for y in range(self.rowCount):
            for x in range(self.columnCount):
                if self.matrix[x][y] == self.EMPTY_CELL:
                    cells.append((x,y))
        return cells
    
    def checkforwin(self, xo):
        # row win
        for x in range(self.columnCount):
            win = True
            for y in range(self.rowCount):
                if self.matrix[x][y] != xo:
                    win = False
                    break
            if win:
                return True
        # column win
        for y in range(self.rowCount):
            win = True
            for x in range(self.columnCount):
                if self.matrix[x][y] != xo:
                    win = False
                    break
            if win:
                return True
        # diagonal win
        if self.rowCount == self.columnCount:
            win = True
            for xy in range(self.rowCount):
                if self.matrix[xy][xy] != xo:
                    win = False
                    break
            if win:
                return True
            # other diagonal win
            win = True
            for xy in range(self.rowCount):
                if self.matrix[xy][self.rowCount-1-xy] != xo:
                    win = False
                    break
            if win:
                return True
    
        return False 