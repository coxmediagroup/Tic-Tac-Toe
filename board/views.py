__author__ = 'marc'

from models import Board


from player.models import Player, AIPlayer
from game.models import Game

from config.settings import *
class BoardView():
    """
    containing object for board and players.
    displays board
    """

    def __init__(self):

        self.board = Board()
        self.game = Game(AIPlayer(deep_blue_game_piece), Player(opponent_game_piece))

    def draw(self):
        """Draw the game board on screen"""
        res = ''
        # ANSI code to clear the screen
        #res += chr(27) + "[2J"
        for position, value in enumerate(self.board.tttboard):
            if value is None:
                res += str(position)
                #sys.stdout.write(str(position))
            else:
                res += str(value)
                #sys.stdout.write(str(value))

            if (position + 1) % 3 != 0:
                res += str('|')
                #sys.stdout.write('|')
            else:
                #print ''

                res += str('\n')
            if position == 2 or position == 5:
                #print '-' * 5

                res += '-' * 5
                res += str('\n')
        return res
