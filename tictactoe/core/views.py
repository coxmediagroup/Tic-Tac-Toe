import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from core.game import Game, PLAYER, COMPUTER

@login_required
def play_game(request):
    context = {}
    context['user'] = request.user
    context['board'] = [0] * 9
    context['json_board_str'] = json.dumps(context['board'])
    return render_to_response('core/play_game.html', context, context_instance=RequestContext(request))

@login_required
def make_move(request):
    board = json.loads(request.GET['board'])
    box = int(request.GET['box'].replace("box_",""))

    game = Game(board)
    game.make_move(box, PLAYER)
    game_over = game.check_game_over()
    if not game_over:
        box = game.best_next_move(COMPUTER)
        game.make_move(box, COMPUTER)
        game_over = game.check_game_over()
    
    result = {}
    result['box'] = str(box)
    result['game_over'] = game_over
    result['board'] = json.dumps(game.get_board())
    return HttpResponse(json.dumps(result), mimetype='application/json')

@login_required
def logout(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

