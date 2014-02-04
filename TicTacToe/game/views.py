from django.shortcuts import render
from django.http import HttpResponse
import simplejson
from django.core.cache import cache

#handles the "start game" view
def start_game(request):
    context = {}
    return render(request, 'game/startgame.html', context)

#handles when player presses "Start Game" button
def launch(request):
    context = {}
    return render(request, 'game/game.html', context)

#loads the current game based on settings in memory
def game_page(request):
    context = {}
    return render(request, 'game/game.html', context)

def ajax_make_move(request):
    if request.is_ajax():
        callback = request.GET.get('callback', '')
        req = {}
        req ['box1'] = cache.get('tictactoe_box1')
        req ['box2'] = cache.get('tictactoe_box2')
        req ['box3'] = cache.get('tictactoe_box3')
        req ['box4'] = cache.get('tictactoe_box4')
        req ['box5'] = cache.get('tictactoe_box5')
        req ['box6'] = cache.get('tictactoe_box6')
        req ['box7'] = cache.get('tictactoe_box7')
        req ['box8'] = cache.get('tictactoe_box8')
        req ['box9'] = cache.get('tictactoe_box9')
        req ['game_state'] = cache.get('tictactoe_game_state')

        response = simplejson.dumps(req)
        response = callback + '(' + response + ');'
    else:
        response = 'fail'

    return HttpResponse(response, mimetype="application/json")


