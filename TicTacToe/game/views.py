from django.shortcuts import render
from django.http import HttpResponse
import simplejson
from django.core.cache import cache
from django.template import Context

import gameboard


def get_game_variables():
    ret = {}
    ret['box1'] = gameboard.get_box_state(1)
    ret['box2'] = gameboard.get_box_state(2)
    ret['box3'] = gameboard.get_box_state(3)
    ret['box4'] = gameboard.get_box_state(4)
    ret['box5'] = gameboard.get_box_state(5)
    ret['box6'] = gameboard.get_box_state(6)
    ret['box7'] = gameboard.get_box_state(7)
    ret['box8'] = gameboard.get_box_state(8)
    ret['box9'] = gameboard.get_box_state(9)
    game_board = cache.get('ttt_game_board')
    ret['game_state'] = game_board.state

    return ret

#handles the "start game" view
def start_game(request):
    context = {}
    return render(request, 'game/startgame.html', context)

#handles when player presses "Start Game" button
def launch(request):
    game_board = gameboard.GameBoard(gameboard.PLAYER_X)
    game_board.computer_move()
    cache.set('ttt_game_board', game_board)

    context = get_game_variables()
    context = {'context': context}
    return render(request, 'game/game.html', Context(context))

#loads the current game based on settings in memory
def game_page(request):
    context = {}
    return render(request, 'game/game.html', context)

#handles user making a move
def ajax_make_move(request, box_choice):
    if request.is_ajax():
        game_board = cache.get('ttt_game_board')
        game_board.last_move = box_choice
        gameboard.try_set_box_state(box_choice, gameboard.opposing_player(game_board.side))
        move = game_board.computer_move()

        ret = get_game_variables()
        response = simplejson.dumps(ret)
    else:
        response = 'fail'

    return HttpResponse(response, mimetype="application/json")


