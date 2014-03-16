import sys
import re
import itertools
import types
import os.path

#Default Strategy, but let user set a diff one in params.
try:
    STRATEGY = os.path.splitext(sys.argv[1])[0]
    if not os.path.exists('./strategies/%s.py' % STRATEGY):
        print 'Warning: That is not a valid strategy file. Going to just use aiStrategy1'
        STRATEGY = 'aiStrategy1'
except:
    STRATEGY = 'aiStrategy1'

class TicTacToe():
    def __init__(self, humanMark=None):
        #self.setStrategy(self, STRATEGY)
        self.chooseSides(humanMark)
        #what stage of the game we are in. 
        self.numTurn = 0 

        #layout of basic info we may need to keep in mind. 
        self.squares = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.availSquares = self.squares
        self.xSquares = set()
        self.oSquares = set()
        self.corners = {1, 3, 7, 9}
        self.center = {5}
        self.edges = {2, 4, 6, 8}
        self.history = []

        #Winning combos I am calling RDCs(Rows, Diagonals, Columns)
        self.RDCs = {'R1': [1, 2, 3],
                'R2': [4, 5, 6],
                'R3': [7, 8, 9],
                'C1': [1, 4, 7],
                'C2': [2, 5, 8],
                'C3': [3, 6, 9],
                'D1': [1, 5, 9],
                'D2': [3, 5, 7]}

        self.board="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\
\n            |           |\n            |           |\n\
     (1)    |    (2)    |    (3)\
\n            |           |\n            |           |\n  -----------------------------------\n            |           |\n            |           |\n\
     (4)    |    (5)    |    (6)\
\n            |           |\n            |           |\n  -----------------------------------\n            |           |\n            |           |\n\
     (7)    |    (8)    |    (9)\
\n            |           |\n            |           |\n\n"

    def chooseSides(self, humanMark):
        self.players = ['X', 'O']
        self.humanMark = humanMark
        while self.humanMark not in self.players:
            self.humanMark = raw_input("Choose a side [X or O]: ").upper()
        print "You picked %s." % self.humanMark
        self.aiMark = [mark for mark in self.players if mark != self.humanMark].pop()
        print "That leaves me with %s." % self.aiMark
        #self.players = itertools.cycle(self.players)

    # Collect player's next move and make sure his response is valid.
    def getMove(self):
        try:
            move = int(raw_input('Pick a spot to mark [1-9]: '))
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
            self.printBoard()
            print 'Winner is Player X!'
            return 'X'
        elif ['O','O','O'] in self.RDCs.values():
            self.printBoard()
            print 'Winner is Player O!'
            return 'O'
        elif not self.availSquares:
            self.printBoard()
            print "It's a tie!"
            return 'tie'
        else: 
            return False

    # Is anyone one spot away from winning?
    # Signals either where to move to win or where one must block.
    def evalDanger(self):
        #dangerousSquares = set()
        dangerousSquares = {'X': [], 'O': []}
        for RDC in self.RDCs:
            mightWin = None
            if ((self.RDCs[RDC].count('X') == 2) and (self.RDCs[RDC].count('O') == 0)):
                mightWin = 'X'
            elif ((self.RDCs[RDC].count('O') == 2) and (self.RDCs[RDC].count('X') == 0)):
                mightWin = 'O'

            if mightWin:
                #print "Watch out! %s is almost all filled up by %s's!" % (RDC, mightWin) 
                dangerousSquares[mightWin].extend([square for square in self.RDCs[RDC] if not isinstance(square, str)])
        return dangerousSquares


    # Assess any opportunities to create a fork (2 routes to win).
    def evalForkability(self):
        forkOpps = {'X': [], 'O': []}
        for square in self.availSquares:
            forkOppX = -1
            forkOppO = -1
            for RDC in self.RDCs:
                if (square in self.RDCs[RDC]) and \
                    ((self.RDCs[RDC].count('X') == 1) and (self.RDCs[RDC].count('O') == 0)):
                        forkOppX += 1
                elif (square in self.RDCs[RDC]) and \
                    ((self.RDCs[RDC].count('O') == 1) and (self.RDCs[RDC].count('X') == 0)):
                        forkOppO += 1

                if forkOppX >= 1:
                    forkOpps['X'].append(square)
                if forkOppO >= 1:
                    forkOpps['O'].append(square)

        #for player, square in forkOpps:
        #    print "forking opportunity for %s at: %d" % (player, square)
        return forkOpps
        
    # Keep track of the winning combinations.  Would help assess 
    # the above the other things.
    def markRDCs(self, square, player):
        for RDC in self.RDCs:
            if square in self.RDCs[RDC]:
                self.RDCs[RDC][self.RDCs[RDC].index(square)] = player

    def printBoard(self):
        #print re.sub('[0-9]', '-', self.board)
        print self.board

    def advanceMove(self, move=None):
        self.whosTurn = self.players[0]
        self.players.reverse()
        if self.whosTurn == 'X':
            self.numTurn += 1
        print "Player %s's turn." % self.whosTurn

        if self.whosTurn == self.aiMark:
            move = self.bestMove()
        elif (move is None) and (self.whosTurn == self.humanMark):
            move = self.getMove()

        if self.whosTurn == 'X':
            self.xSquares.add(move)
        else:
            self.oSquares.add(move)

        self.availSquares.discard(move)
        self.markRDCs(move, self.whosTurn)
        self.board = self.board.replace('(%s)' % str(move), ' %s ' % self.whosTurn)
        self.history.append(move)

    def setStrategy(self, stratFile):
        #Pull in strategy and it's corresponding bestMove() function
        exec "from strategies import %s" % stratFile
        newBestMove = eval("%s.bestMove" % stratFile)
        #set its bestMove function as TicTacToe's bestMove() function.
        return setattr(self, newBestMove.__name__, types.MethodType(newBestMove, self))

if __name__ == '__main__':
    game=TicTacToe()
    game.setStrategy(STRATEGY)
    while not game.gameOver():
        game.printBoard()
        game.advanceMove()

        
