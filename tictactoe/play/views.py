from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

import play.utilities as util
from play.models import Game

# Create your views here.
def index(request):
    return render(request, "index.html")

def new_game(request):
    try:
        request.session['board_id'] = util.new_game()
    except:
        return util.json_response(False, "New game not created.")
    return util.json_response(True, "New game created:" + str(request.session['board_id']))

def get_details(request):
    import json
    if 'board_id' not in request.session:
        request.session['board_id'] = util.new_game()
    game = Game.objects.get(id=request.session['board_id'])
    response = {
        'board': game.board,
        'game_count': game.game_count,
        'draw_count': game.draw_count
    }
    return HttpResponse(json.dumps(response))

def move(request):
    import re
    import strategy
    #import movelogic

    if ('cell' not in request.POST) \
            or (re.search('^[0-8]$', request.POST['cell']) is None):
        raise Http404
    cell = int(request.POST['cell'])

    # Make sure we have an active game
    if 'board_id' not in request.session:
        try:
            util.new_game()
        except:
            return util.json_response(False, "New game not created.")
    else:
        # verify we have a valid game id
        try:
            game = Game.objects.get(id=request.session['board_id'])
        except:
            return util.json_response(False, "Invalid game.")
    
    plan = strategy.Strategy(game.board)
    # Prevent the user from moving to a space that has already been used
    if not plan.cell_available(cell):
        return util.json_response(False, "Invalid move.  You naughty hacker.")
    plan.move('x', cell)
    next_move = str(plan.next_move())
    game_state = plan.game_state()
    game.board = plan.board
    if game_state != "in-play":
        game.board = "         "
        game.game_count = game.game_count + 1
        if game_state == "draw":
            game.draw_count = game.draw_count + 1
    game.save()
    
    # At this point we have an active game -- use it!
    return util.json_response(True, "OK", next_move, game_state)
