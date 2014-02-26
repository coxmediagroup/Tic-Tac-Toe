__author__ = 'marc'

from board.models import Board
from config.settings import *
def check_for_win(board, player):
    """Check the board to see if the player has won"""
    winner = False
    for group in WINS:
        if board.tttboard[group[0]] == player.board_value \
                and board.tttboard[group[1]] == player.board_value \
                and board.tttboard[group[2]] == player.board_value:
            winner = True
            break

    return winner
