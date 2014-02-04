from django.shortcuts import render
from django.http import HttpResponse
import simplejson
from django.core.cache import cache

import gameboard
game_board = gameboard.GameBoard()


#handles the "start game" view
def start_game(request):
    context = {}
    return render(request, 'game/startgame.html', context)

#handles when player presses "Start Game" button
def launch(request):
    game_board.reset()

    return render(request, 'game/game.html')

#loads the current game based on settings in memory
def game_page(request):
    context = {}
    return render(request, 'game/game.html', context)

#handles user making a move
def ajax_make_move(request):
    if request.is_ajax():
        req = {}
        req['box1'] = game_board.get_box_state(1)
        req['box2'] = game_board.get_box_state(1)
        req['box3'] = game_board.get_box_state(1)
        req['box4'] = game_board.get_box_state(1)
        req['box5'] = game_board.get_box_state(1)
        req['box6'] = game_board.get_box_state(1)
        req['box7'] = game_board.get_box_state(1)
        req['box8'] = game_board.get_box_state(1)
        req['box9'] = game_board.get_box_state(1)
        req['game_state'] = game_board.state

        response = simplejson.dumps(req)
    else:
        response = 'fail'

    return HttpResponse(response, mimetype="application/json")


