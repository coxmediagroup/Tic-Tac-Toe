from django.shortcuts import render_to_response
from django.template import RequestContext

from tic_tac_toe.game import TicTacToe

def gameboard(request, template_name='ticky/game.html'):
    game = request.session.get('tic_tac_toe_game', None)
    if not game:
        game = TicTacToe()
    return render_to_response(template_name, RequestContext(request, {
        'game': game
    }))
