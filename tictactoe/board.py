class Board(object):
    '''
    The board class represents a tic tac toe board. The class shall be backed
    by a size 9 'array' holding 3 rows of 3 columns. The indices are defined as
    follows:
     0 | 1 | 2
     --+---+--
     3 | 4 | 5
     --+---+--
     6 | 7 | 8
    '''
    WIN=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

    def __init__(self):
        self.board=['']*9
        self.moves=[]

    def __str__(self):
        grid=''
        for y in range(0,3):
            line=''
            for x in range(0,3):
                line+=' ' if self.board[y*3+x]=='' else self.board[y*3+x]
                if x < 2:
                    line+=' | '
            grid+=line
            if y < 2:
                grid+='\n--+---+--\n'
        return grid

    def __repr__(self):
        return self.__str__()

    def mark(self, location, markType):
        self.board[location]=markType
        self.moves.append((location,markType))

    def isMarked(self, location):
        return location >= 0 and location < 9 and self.board[location] != ''

    def isFilled(self):
        return all(''!=i for i in self.board)

    def isWinner(self, markType):
        #return True if the markType (x,o) has a winning position
        for c in self.WIN:
            if(all(markType == self.board[i] for i in c)):
                return True;
        return False
    
    def isEmptyExcept(self, locations):
        marks=range(0,9)
        [marks.remove(l) for l in locations]
        return all('' == self.board[i] for i in marks)