"""
    Tests for board.py and bot.py game representations.

    Mostly to assure that the AI loses under no circumstances.

    Check every possible move for a player win.

    First player moves on even depths.

    Second player moves on odd depths.
"""

import pprint

import board
import bot 


def test_moves(game, player='x'):
    # if the game is over, return
    if game.depth == 9 or game.winner:
        return

    # if it is the players turn, loop through and check each possible move
    if (player == 'x' and game.depth % 2 == 0) or \
        (player == 'o' and game.depth % 2 == 1):
            for move in game.get_legal_moves():
                gameprime = game.apply_move(move)
                try:
                    assert gameprime.winner != player
                except:
                    print gameprime
                test_moves(gameprime, player)
    #if it's the bot's turn
    else:
        gameprime = bot.get_next_gamestate(game)
        try:
            assert gameprime.winner != player
        except:
            print gameprime
        test_moves(gameprime, player)


if __name__ == '__main__':
    game = board.TTTGameBoard()
    print "Player First"
    test_moves(game)
    print "Player Second"
    test_moves(game,player='o')

