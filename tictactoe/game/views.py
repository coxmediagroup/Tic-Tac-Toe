"""
Views for Tic-Tac-Toe game
"""
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from tictactoe.game import logic
from tictactoe.game.decorators import ajax_required

__author__ = "Nick Schwane"


def json_response(content):
    """
    Returns HttpResponse with JSON content
    """
    return HttpResponse(content, mimetype="application/json")


def main_view(request):
    """
    Returns page for tic-tac-toe game
    """
    return render_to_response('game/main.html', {}, context_instance=RequestContext(request))


@ajax_required
def computer_move(request):
    """
    AJAX view used to calculate computer player's next move
    """
    board, mark = logic.construct_board(request)
    position, win = logic.determine_computer_move(board, mark)
    board[position] = mark if position != -1 else board[position]
    draw = position == -1 or ' ' not in board
    return json_response(json.dumps(
                                    {'position': position,
                                     'is_winner': win,
                                     'is_draw': draw}
                                    ))


@ajax_required
def human_move(request):
    """
    AJAX view used to determine if human's move has won
    """
    board, mark = logic.construct_board(request)
    win = logic.check_for_win(board, mark)
    return json_response(json.dumps({'is_winner': win}))


