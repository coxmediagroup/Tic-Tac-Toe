"""
This is a Tic-Tac-Toe game
Enjoy!!
"""
import itertools
from ai import ComputerPlayer, Player
from board import Board, X, O, STALEMATE

class HumanPlayer(Player):
    def select_move(self, board):
        print "Enter a move for %s:" % self.player_symbol
        available = [str(c) for c in board.cells() if c not in (X, O)]
        return take_input("Space", available)


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
