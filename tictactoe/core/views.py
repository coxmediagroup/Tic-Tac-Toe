import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from core.game import Game, PLAYER, COMPUTER
from core.models import GameHistory

@login_required
def play_game(request):
    context = {}
    user = request.user

    game_history = GameHistory.objects.create(player=user)

    all_games = GameHistory.objects.filter(player=user)
    context['played'] = all_games.count()
    context['won'] = all_games.filter(status='won').count()
    context['lost'] = all_games.filter(status='lost').count()
    context['tied'] = all_games.filter(status='tied').count()
    context['not_completed'] = all_games.filter(status='in_progress').count()
    

    context['user'] = user
    context['game_history_id'] = game_history.id
    context['board'] = [0] * 9
    context['json_board_str'] = json.dumps(context['board'])
    return render_to_response('core/play_game.html', context, context_instance=RequestContext(request))

@login_required
def make_move(request):
    board = json.loads(request.GET['board'])
    box = int(request.GET['box'].replace("box_",""))
    game_history_id = request.GET['game_history_id']

    game = Game(board)
    game.make_move(box, PLAYER)
    game_over = game.check_game_over()
    if not game_over:
        box = game.best_next_move(COMPUTER)
        game.make_move(box, COMPUTER)
        game_over = game.check_game_over()

    if game_over:
        game_history = GameHistory.objects.get(pk=game_history_id)
        game_history.finish_game(game_over)
    
    result = {}
    result['box'] = str(box)
    result['game_over'] = game_over
    result['board'] = json.dumps(game.get_board())
    return HttpResponse(json.dumps(result), mimetype='application/json')

@login_required
def logout_user(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

