import sys
import re
import itertools

class TicTacToe():
    def __init__(self):
        #what stage of the game we are in. 
        self.numTurn = 1 

        #layout of basic info we may need to keep in mind. 
        self.squares = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.availSquares = self.squares
        self.xSquares = set()
        self.oSquares = set()
        self.corners = {1, 3, 7, 9}
        self.center = {5}
        self.edges = {2, 4, 6, 8}

        #Winning combos I am calling RDCs(Rows, Diagonals, Columns)
        self.RDCs = {'R1': [1, 2, 3],
                'R2': [4, 5, 6],
                'R3': [7, 8, 9],
                'C1': [1, 4, 7],
                'C2': [2, 5, 8],
                'C3': [3, 6, 9],
                'D1': [1, 5, 9],
                'D2': [3, 5, 7]}

        self.board="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\
1    |    2    |    3\
\n     |         |\n     |         |\n---------------------\n     |         |\n     |         |\n\
4    |    5    |    6\
\n     |         |\n     |         |\n---------------------\n     |         |\n     |         |\n\
7    |    8    |    9"

    # Collect player's next move and make sure his response is valid.
    def getMove(self):
        try:
            move = int(raw_input('Pick a spot: '))
        except ValueError:
            print 'Try Again'
            move = self.getMove() 
        
        if move not in self.availSquares:
            print 'That was not an available space.  Pick one that does not have an X or O in it already.'
            move = self.getMove()

        return move

    # Did somebody win? Is it a tie?
    def gameOver(self):
        if ['X','X','X'] in self.RDCs.values():
            print 'Winner is Player X!'
            sys.exit(0)
        elif ['O','O','O'] in self.RDCs.values():
            print 'Winner is Player O!'
            sys.exit(0)
        elif not self.availSquares:
            print "It's a tie!"
            sys.exit(0)
        else: 
            return False

    # Is anyone one spot away from winning?
    # Signals either where to move to win or where one must block.
    def evalDanger(self):
        for RDC in self.RDCs:
            mightWin = None
            if ((self.RDCs[RDC].count('X') == 2) and (self.RDCs[RDC].count('O') == 0)):
                mightWin = 'X'
            elif ((self.RDCs[RDC].count('O') == 2) and (self.RDCs[RDC].count('X') == 0)):
                mightWin = 'O'

            if mightWin:
                print "Watch out! %s is almost all filled up by %s's!" % (RDC, mightWin) 

    # Assess any opportunities to create a fork (2 routes to win).
    def forkability(self):
        pass

    # Keep track of the winning combinations.  Would help assess 
    # the above the other things.
    def markRDCs(self, square, player):
        for RDC in self.RDCs:
            if square in self.RDCs[RDC]:
                self.RDCs[RDC][self.RDCs[RDC].index(square)] = player

if __name__ == '__main__':
    game=TicTacToe()
    players = itertools.cycle(['X', 'O'])
    while not game.gameOver():
        print re.sub('[0-9]', '-', game.board)
        #print game.board
        player = players.next()
        print game.RDCs
        game.evalDanger()
        print "Player %s's turn." % player
        move = game.getMove()
        game.availSquares.discard(move)
        game.markRDCs(move, player)
        game.board = game.board.replace(str(move), player)
        
        
        
    







