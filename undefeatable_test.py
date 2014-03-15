from TicTacToe import *
import copy

'''
Unit test that simultaneously plays out every game possibility.

Idea is:
    1) Initiatie a game
    2) progress through it until human/user is to make a choice about where to move
    3) see how many available squares they are, and for each available move, make a clone of the game and mark that available square in the clone. The list of clones replace the original game they branched from. Until a clone wins. 
    4) Repeat 2) and 3) until each game possibility/branch/universe is played out
'''

class TTTTest:
    def __init__(self):
        self.games = [] #Main list of all currently active games
        self.games.append(TicTacToe()) #Initiate a game.  No moves yet.
        self.tally = {'X': 0, 'O': 0, 'tie': 0, 'badGames': []}

    #Branch a game: create all possible branches based on available squares.
    def branchGame(self, game):
        pass

    #Branch all games in the main game list
    def branchAllGames(self):
        pass

