import sys
import re
import itertools
import random

class TicTacToe():
    def __init__(self, humanMark=None):
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

        self.board="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\
1    |    2    |    3\
\n     |         |\n     |         |\n---------------------\n     |         |\n     |         |\n\
4    |    5    |    6\
\n     |         |\n     |         |\n---------------------\n     |         |\n     |         |\n\
7    |    8    |    9"

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
            move = int(raw_input('Pick a spot [1-9, left to right and top to bottom.  1 is top left, 9 is bottom right]: '))
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
            return 'X'
            sys.exit(0)
        elif ['O','O','O'] in self.RDCs.values():
            print 'Winner is Player O!'
            return 'O'
            sys.exit(0)
        elif not self.availSquares:
            print "It's a tie!"
            return 'tie'
            sys.exit(0)
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
                print "Watch out! %s is almost all filled up by %s's!" % (RDC, mightWin) 
                dangerousSquares[mightWin].extend([square for square in self.RDCs[RDC] if not isinstance(square, str)])
                #dangerousSquares.add(mightWin, [square for square in self.RDCs[RDC] if not isinstance(square, str)][0])
        return dangerousSquares


    # Assess any opportunities to create a fork (2 routes to win).
    def evalForkability(self):
        #forkOpps = set()
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
                    #forkOpps.add(('X', square)) 
                    forkOpps['X'].append(square)
                if forkOppO >= 1:
                    #forkOpps.add(('O', square))
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

    # Strategize and make best move.
    # If it's my first turn, don't bother with rest, what's the best first
    # move for O and X?
    # 1) Can I win? [Danger in my benefit]
    # 2) Can human win? [Danger for human benefit, must block if so]
    # 3) Can I fork?
    # 4) What?
    def bestMove(self):
        if self.numTurn == 1:
#            if self.aiMark == 'X':
#                return random.choice(list(self.corners))
            if self.aiMark == 'O':
                if self.center & self.availSquares:
                    return list(self.center).pop()
                    
        dangerousSquares = self.evalDanger()
        forkOpps = self.evalForkability()

        #If I can win, take the first available winning box!
        if dangerousSquares[self.aiMark]:
            return dangerousSquares[self.aiMark][0]
        #If I can't win but human can on his next turn, block the first danger!!
        elif dangerousSquares[self.humanMark]:
            return dangerousSquares[self.humanMark][0]
        #Can I create a fork?
        elif forkOpps[self.aiMark]:
            return forkOpps[self.aiMark][0]
        
        elif self.numTurn == 2:
            if self.aiMark == 'O':
                #If both X's are in corners, we know O is in middle.  Take an edge
                if len(self.corners & self.xSquares) == 2:
                    return random.choice(list(self.edges & self.availSquares))
        #Can I create a dangerous situation?

        #Can my opponent create a fork on his next turn? If so, take one of his forks?
        if forkOpps[self.humanMark]:
            return forkOpps[self.humanMark][0]

        #Do something else if none of the above
        else:
            return self.availSquares.pop()


    def printBoard(self):
        print re.sub('[0-9]', '-', self.board)
        #print self.board

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
        self.board = self.board.replace(str(move), self.whosTurn)
        self.history.append(move)

if __name__ == '__main__':
    game=TicTacToe()
    while not game.gameOver():
        game.printBoard()
        game.advanceMove()

        
        


