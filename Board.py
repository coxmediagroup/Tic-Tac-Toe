from TicTacToeExceptions import TokenPlacementException
from Judge import Judge
import random
import copy

class Board(object):

    def __init__(self, player=None, computer=None):
        self.tokens = [' '] * 9
        self.player_token = player
        self.computer_token = computer
        self.judge = Judge(self)

    def playAgain(self):
        """Find out if we want another go"""
        print('Do you want to play again? (yes or no)')
        return self._raw_input().lower().startswith('y')

    def isWinner(self):
        """Did a win just happen?"""
        result = self.judge.evalGame()
        if result[0] is not None:
            return 'win'
        elif result == [None, None]:
           return False
        else:
            return 'draw'

    def makeComputerMove(self, brain):
        """Make the computer's move"""
        results = []
        tokens = copy.copy(self.tokens)
        if self.take_center():
            best = 4
        else:
            brain.evaluateMove(p=self.computer_token, board=tokens)
            best = brain.best_move
        self.addToken(self.computer_token, int(best))
        print self.drawBoard()

    def take_center(self):
        """figure out if we can have the center square
        rather than calculating the whole tree our first
        move"""
        token_count = self.tokens.count(' ')
        if token_count == 9:
            return True
        elif token_count == 8 and self.tokens[4] == ' ':
            return True
        return False

    def getPlayerMove(self):
        """Get the player's move"""
        move = ' '
        while move not in self.getPossibleMoves():
            print('What is your next move? (1-9)')
            move = self._raw_input()
            try:
                int(move)
            except:
                print "Please enter a digit"
                print self.drawBoard()
                continue
            try:
                self.addToken(self.player_token, int(move) - 1)#make the move into an index of the board
                print self.drawBoard()
                break
            except TokenPlacementException:
                print "please select an empty spot"
                print self.drawBoard()


    def firstMove(self):
        """Computer goes first"""
        which = random.randint(1, 2)
        if which == 1:
            return 'computer'
        else:
            return 'player'

    def drawBoard(self):
        """Draw a tic-tac-toe board"""

        b = '\n\n%s|%s|%s\n' % tuple(self.tokens[:3])
        b += '_____\n'
        b += '%s|%s|%s\n' % tuple(self.tokens[3:6])
        b += '_____\n'
        b += '%s|%s|%s\n\n' % tuple(self.tokens[6:])

        return b

    def addToken(self, token, idx):
        """Add a token to the board or raise an exception

        str token  "x" or "o"
        int idx    0-8"""

        idx = int(idx)
        if  idx > 8 or idx < 0:
            msg = "Invalid index %s " % idx
            raise TokenPlacementException(msg)

        if self.tokens[idx] == ' ':
            self.tokens[idx] = token
        else:
            msg = "Token at %s" % idx
            raise TokenPlacementException(msg)

    def getBoard(self):
        return copy.copy(self.tokens)

    def getPossibleMoves(self):
        """Return the indexes of possible moves"""
        result = list()
        for i in range(9):
            if self.tokens[i] == ' ':
                result.append(i)
        return result

    def inputPlayerLetter(self):
        """Allow the player to choose a letter"""
        letter = ''
        while not (letter == 'X' or letter == 'O'):
            print('Do you want to be X or O?')
            letter = self._raw_input()
            letter = letter.upper()
            if letter == 'X':
                self.player_token = letter
                self.computer_token = 'O'
                break
            elif letter == 'O':
                self.player_token = letter
                self.computer_token = 'X'
                break

    def _raw_input(self):
        return raw_input()
