"""
implements tic-tac-toe board
"""

EMPTY_MARKER = '?'

class Board:
    """
    Tic-Tac-Toe board
    Interact with it primarily through the move and finished functions
    """

    def __init__(self):
        self.emptyMarker = EMPTY_MARKER#this is really only here to pass to minimax easily
        self.reset()

    def printBoardCLI(self):
        """
        really just for debugging
        """
        for y in self.board:
            print y

    def reset(self):
        self.board = [[self.emptyMarker]*3 for i in range(3)]

    def move(self, player, x, y):
        """
        play move at (x,y)
        player is either 'X' or 'O'
        """
        if x < 0 or x > 2 or y < 0 or y > 2:
            raise IndexError("x and y must be between 0 and 2, inclusive")
        if self.board[y][x] != self.emptyMarker and player != self.emptyMarker:
            raise ValueError("Can't move at (%d,%d), it's already taken by %s"%(x,y,self.board[y][x]))
        self.board[y][x] = player

    def getEmptySquares(self):
        """
        all available moves, makes minimax simpler
        """
        return [(x,y) for x in range(3) for y in range(3) if self.board[y][x]==self.emptyMarker]

    def finished(self):
        """
        whether there's a winner or a tie
        returns a tuple of (<whether game finished>, <winner>)
        if the game isn't finished or is tied, winner is None
        """
        #test horizontal
        for y in range(3):
            marker = self.board[y][0]
            if marker != self.emptyMarker and all(mark==marker for mark in self.board[y]):
                return True, marker 
        #test vertical
        for x in range(3):
            marker = self.board[0][x]
            if marker != self.emptyMarker and all(mark==marker for mark in [self.board[y][x] for y in range(3)]):
                return True, marker
        #test diagonals
        marker = self.board[1][1]
        if marker != self.emptyMarker:
            corners = [[self.board[0][0],self.board[2][2]],[self.board[0][2],self.board[2][0]]]
            for diagonal in corners:
                if all(mark == marker for mark in diagonal):
                    return True, marker 
        #no winner, check for tie
        if all(self.board[x][y] != self.emptyMarker for x in range(3) for y in range(3)):
            return True, None
        #no winner, no tie
        return False, None
