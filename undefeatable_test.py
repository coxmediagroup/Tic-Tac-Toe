'''
Unit test that simultaneously plays out every game possibility.

Idea is:
    1) Initiatie a game
    2) progress through it until human/user is to make a choice about where to move
    3) see how many available squares they are, and for each available move, make a clone of the game and mark that available square in the clone. The list of clones replace the original game they branched from. Until a clone wins. 
    4) Repeat 2) and 3) until each game possibility/branch/universe is played out
'''

import sys
import os
import copy
try:
    STRATEGY = os.path.splitext(sys.argv[1])[0]
except IndexError:
    STRATEGY = 'aiStrategy1'

if not os.path.exists('./strategies/%s.py' % STRATEGY):
    print 'Warning: That is not a valid strategy file in the strategies folder. Canceling test.'
    sys.exit(0)

from TicTacToe import *


class TTTTest:
    def __init__(self):
        self.games = [] #Main list of all currently active games
        self.games.append(TicTacToe('X')) #Initiate a game.  No moves yet. X is human player.
        self.games.append(TicTacToe('O')) #Initiate a game.  No moves yet. O is human player.
        self.tally = {'X-wins': 0, 'O-wins': 0, 'badGames': [], 'X-ties': 0, 'O-ties': 0, 'X-loss': 0, 'O-loss': 0}

        for game in self.games:
            game.setStrategy(STRATEGY)

    #Branch a game: create all possible branches based on available squares.
    def branchGame(self, game):
        branches = []

        #If not human turn, advance move
        #If next player is ai, go ahead and play his turn
        if game.players[0] == game.aiMark:
            game.advanceMove()

        #If game is over, don't bother branching, kill this game / return empty branches to replace it.
        if self.checkGameOver(game):
            return branches
        else:
            #Game is not over, so for eacy available move make a copy game and make that move.
            #If that move ended the game, don't bother passing on/keeping that branch/clone. It died in infancy.
            for square in game.availSquares:
                x = copy.deepcopy(game)
                x.advanceMove(move=square)
                if not self.checkGameOver(x):
                    branches.append(x)

            return branches

    #Branch all games in the main game list
    def branchAllGames(self):
        newGameBranches = []
        for game in self.games:
            #If game is not over, branch it, replace its place in the ongoing games list with its living children.
            if not self.checkGameOver(game):
                newGameBranches.extend(self.branchGame(game))
        self.games = newGameBranches

    #Check if given game is over.  If it is, tally the result.
    def checkGameOver(self, gameInst):
        status = gameInst.gameOver()
        if not status:
            #Game is not over
            return False
        else:
            #Game is over.  Tally results
            if gameInst.humanMark == status:
                self.tally['badGames'].append(gameInst)
                self.tally['%s-loss' % gameInst.aiMark] += 1
            elif gameInst.aiMark == status:
                self.tally['%s-wins' % status] += 1
            else: #Tie
                self.tally['%s-ties' % gameInst.aiMark] += 1
            return True

    #Traverse through all possible games trajectories.
    def runTest(self):
        #Keep branching until we are left with nothing in the ongoing games list.
        while self.games:
            self.branchAllGames()

        self.printResults()

    def printResults(self):
        print "===================================================================================================="
        print 'Games AI won as X: %d' % self.tally['X-wins']
        print 'Games AI won as O: %d' % self.tally['O-wins']
        print 'Games AI lost as X: %d' % self.tally['X-loss']
        print 'Games AI lost as O: %d' % self.tally['O-loss']
        print 'Games tied when AI was X: %d' % self.tally['X-ties']
        print 'Games tied when AI was O: %d' % self.tally['O-ties']
        print 'Total AI wins: %d' % (self.tally['X-wins'] + self.tally['O-wins'])
        print 'Total ties: %d' % (self.tally['X-ties'] + self.tally['O-ties'])
        print "===================================================================================================="

        failures = len(self.tally['badGames'])
        if failures > 0:
            print 'FAIL: AI lost in %d scenarios!' % failures 
        else:
            print 'PASS: AI never lost!' 
    

if __name__ == '__main__':
    #Redirect output to log
    stdout = sys.stdout
    log = open('log.txt', 'w')
    sys.stdout = log

    test = TTTTest()
    test.runTest()
    #Output back to stdout
    sys.stdout = stdout
    log.close()
    test.printResults()



