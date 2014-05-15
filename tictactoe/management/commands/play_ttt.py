from django.core.management.base import BaseCommand

#from tictactoe import Player, AIPlayer, Board, play_game
import tictactoe as ttt

class Command(BaseCommand):
    """Management command to play a game of Tic Tac Toe"""

    def handle(self, *args, **kwargs):
        ttt.play_game(ttt.Board(), ttt.AIPlayer('X'), ttt.Player('Y'))
