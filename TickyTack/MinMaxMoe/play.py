"""
Simple stdio interface for playing tic tac toe.

This uses a minimax algorithm.
"""
import sys, anydbm

## sanity check ###########################################

try:
    from MinMaxMoe.tictactoe import TicTacToe, X, O, kBlank, otherSide
except ImportError:
    print "ERROR: Couldn't load MinMaxMoe.tictactoe."
    print "Maybe try 'cd ..' first?"
    sys.exit()
try:
    from MinMaxMoe.gentree import kDbmName
    gDbm = anydbm.open(kDbmName)
except:
    print "ERROR: Couldn't load %s" % kDbmName
    print "Maybe try 'python MinMaxMoe/gentree.py' first?"

from MinMaxMoe.bots import *


## user interface code ####################################

kColNames = 'ABC'
kRowNames = '123'


def h1(text):
    print
    print '=' * len(text)
    print text
    print '=' * len(text)
    print


def h2(text):
    print
    print text
    print '-' * len(text)


def h3(text):
    print
    print '[ %s ]' % text


def playAgainP():
    answer = "???"
    while answer not in "YN":
        answer = raw_input("Want to keep playing? [Y|N]: ").strip().upper()
    return bool(answer == "Y")


def fancyPrint(game):
    """
    Like so:
    
         A   B   C
       _____________
      |             |
    1 |  X :   : O  |
      | ---+---+--- |
    2 |    : O :    |
      | ---+---+--- |
    3 |    :   :    |
      |_____________|
    """
    print '     A   B   C   '
    print '   _____________ '
    print '  |             |'
    ##### 'i |  s : s : s  |'
    for i, row in enumerate(game.data):
        args = tuple([i + 1] + [v if v != kBlank else ' ' for v in row])
        assert len(args) == 4
        print '%s |  %s : %s : %s  |' % args
        if i < 2:
            print '  | ---+---+--- |'
    print '  |_____________|'


def playerTurn(side, game):
    assert side in (X, O)
    move = None
    h3('Your turn.')
    fancyPrint(game)
    ex = game.moves[0][1:]
    while not move in game.moves:
        if move is not None:
            print 'Invalid move. Valid moves are:'
            print [move[1:] for move in game.moves] # strip the X/O prefix
        move = side + raw_input("Your move? [ex: '%s']: " % ex).strip().upper()
    return getattr(game, move)


def botTurn(bot, game):
    h3("%s's turn." % bot.name)
    move = bot.choose(game)
    h3('%s places %s at %s' % (bot.name, move[0], move[1:]))
    return getattr(game, move)


## main loop ##############################################


def main(bot):
    keepPlaying = True
    player = X
    h1('%s accepts your challenge!' % bot.name)
    while keepPlaying:
        game = TicTacToe()
        h2("Starting New Game!")
        h3("You are playing as %s." % player)
        while not game.isOver:
            if game.toPlay == player:
                game = playerTurn(player, game)
            else:
                game = botTurn(bot, game)
            h3(game.currentState)
        player = otherSide(player)
        keepPlaying = playAgainP()
    h3('Thank you for playing. Goodbye.')


if __name__=="__main__":
    main(MinMaxMoeBot(gDbm, verbose=True))

