"""
This is a Tic-Tac-Toe game
Enjoy!!
"""
import itertools
from board import Board, X ,O, E, STALEMATE
class HumanPlayer(object):
    """docstring for Player"""
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol
    def move(self, board):
        print "Enter a move for %s:" % self.player_symbol
        r = int(take_input("Row", ('0','1','2')))
        c = int(take_input("Col", ('0','1','2')))
        print "Player %s is playing at (%s,%s)" %(self.player_symbol, r, c)
        board.move(self.player_symbol, int(r), int(c))

class ComputerPlayer(object):
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol
        raise Exception("Stub not implemented")

def take_input(prompt, options):
    while True:
        val = raw_input(prompt + str(options) + ':')
        if val.upper() in options:
            return val.upper()

intro=r"""
 __          ______  _____  _____
 \ \        / / __ \|  __ \|  __ \
  \ \  /\  / / |  | | |__) | |__) |
   \ \/  \/ /| |  | |  ___/|  _  /
    \  /\  / | |__| | |    | | \ \
     \/  \/   \____/|_|    |_|  \_\

Would you like to play a game?
I only know Tic-Tac-Toe

"""

def select_player(symbol):
    print "Who should play %s?" % symbol
    p = take_input("Human or Computer?", ('H', 'C'))
    if p == 'H':
        return HumanPlayer(symbol)
    else:
        return ComputerPlayer(symbol)

def  tic_tac_toe():

    pX = select_player(X)
    pO = select_player(O)

    board = Board()
    winner = None
    print board
    for player in itertools.cycle( (pX, pO) ):
        player.move(board)
        print board
        winner = board.check_win()
        if winner:
            break
    if winner not in (X,O):
        print "Stale Mate"
        print "A curious game."
        print "The only way to win is not to play."
        print "How about a nice game of Global Thermonuclear Warfare?"
        print ""
    else:
        print "%s Wins!" % winner

if __name__ == '__main__':
    print intro
    playagain = "Y"
    while playagain.upper() == "Y":
        tic_tac_toe()
        playagain = take_input("Play Again?", ('Y','N'))
