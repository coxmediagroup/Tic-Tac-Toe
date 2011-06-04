"""
Views for Tic-Tac-Toe game
"""
import json
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext

__author__ = "Nick Schwane"

CORNERS = [0, 2, 6, 8]
EDGES = [1, 3, 5, 7]
CENTER = 4
WINNERS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
 
 
def main_view(request):
    """
    Returns page for tic-tac-toe game
    """
    return render_to_response('game/main.html', {}, context_instance=RequestContext(request))


def computer_move(request):
    if request.is_ajax():
        board = []
        for i in range(0, 9):
            board.append(request.GET.get(str(i), ' '))
        mark = request.GET.get('mark')
        position, win = _determine_move(board, mark)
        json_str = json.dumps({'position': position, 'is_winner': win})
        response = HttpResponse(json_str, mimetype="application/json")
        return response
    else:
        return HttpResponseForbidden('Forbidden')


def check_for_win():
    pass

def _determine_move(board, mark):
    """
    Determines next move for computer player
    
    Returns tuple of next move and boolean if it creates a winning condition.
    """
    WIN = True
    NO_WIN = False
    
    # check for winner
    for possible in range(0, 9):
        if board[possible] == ' ':        
            for winner in WINNERS:
                winner = winner[:]
                if possible in winner:
                    winner.remove(possible)
                    if board[winner[0]] == mark and board[winner[1]] == mark:
                        return possible, WIN
            
    # check for block
    
    # check for empty cell
    for possible in range(0, 9):
        if board[possible] == ' ':
            return possible, NO_WIN
    
    # no possible move
    return -1, NO_WIN