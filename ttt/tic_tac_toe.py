class TicTacToe:
    def __init__(self, xo='X', first=False):
        self.board = [[None]*3, [None]*3, [None]*3]
        self.xo = xo
        if first:
            self.ai_move()

    def output(self):
        """
        Print the board.
        """
        for i in range(3):
            print self.board[i]

    def has_win_move(self, mark='O'):
        """
        mark has a move where they can win
        
        Returns a where to place the opposite mark to bloack the win.
        """

        # First along the x axis
        for i in range(3):
            if self.places_match([(i, 0, mark), (i, 1, mark), (i, 2, None)]):
                return (i, 2)
            if self.places_match([(i, 1, mark), (i, 2, mark), (i, 0, None)]):
                return (i, 0)

        # Then along the y axis
        for i in range(3):
            if self.places_match([(0, i, mark), (1, i, mark), (2, i, None)]):
                return (2, i)
            if self.places_match([(1, i, mark), (2, i, mark), (0, i, None)]):
                return (0, i)

        # Now diagonal
        # (1,1) is always going to be set for diagonals, all we need to do is
        # match the corners.
        # TODO - I should propbably test that the open value is actualy None
        diagonals = {(0, 0): (2, 2),
                     (2, 2): (0, 0),
                     (0, 2): (2, 0),
                     (2, 0): (0, 2)}

        for diags, ret in diagonals.items():
            if self.places_match([(diags[0], diags[1], mark), (1, 1, mark)]):
                return ret

        return False

    def has_fork(self, mark='O'):    
        """
        A fork is when there exists two possibilities that create a winning
        move. 
        
        They are either a diagonal and straight or two straights.
        """

        forks = [[(0, 0), (1, 0), (2, 0), (1, 1), (2, 2)],
                 [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2)],
                 [(0, 0), (0, 1), (0, 2), (1, 1), (2, 2)],
                 [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)]]

#        for fork in forks:
#            missing = []
#            for f in fork:
#
    def places_match(self, places):
        """
        Check if the places are taken by xo.

        places is a list of tuple of (x,y,xo).
        """
        found=True
        if not places:
            return False

        for place in places:
            x, y, xo = place
            if self.board[x][y] != xo:
                found = False

        return found



    def ai_move(self):
        if self.xo == 'X':
            opponent = 'O'
        else:
            opponent = 'X'

        # win move for me
        where = self.has_win_move(mark=self.xo)
        if where:
            self.board[where[0]][where[1]] = self.xo
