"""
Views for Tic-Tac-Toe game
"""
import json
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from tictactoe.game import logic

__author__ = "Nick Schwane"
 
 
def main_view(request):
    """
    Returns page for tic-tac-toe game
    """
    return render_to_response('game/main.html', {}, context_instance=RequestContext(request))


def computer_move(request):
    """
    AJAX view used to calculate computer player's next move
    """
    if request.is_ajax():
        board, mark = logic.construct_board(request)
        position, win = logic.determine_computer_move(board, mark)
        json_str = json.dumps({'position': position, 'is_winner': win})
        response = HttpResponse(json_str, mimetype="application/json")
        return response
    else:
        return HttpResponseForbidden('Forbidden')


def human_move(request):
    """
    AJAX view used to determine if human's move has won
    """
    if request.is_ajax():
        board, mark = logic.construct_board(request)
        win = logic.check_for_win(board, mark)
        json_str = json.dumps({'is_winner': win})
        response = HttpResponse(json_str, mimetype="application/json")
        return response
    else:
        return HttpResponseForbidden('Forbidden')


