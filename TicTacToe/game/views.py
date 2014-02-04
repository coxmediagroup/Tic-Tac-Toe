from django.shortcuts import render
from django.http import HttpResponse
import simplejson
from django.core.cache import cache
from django.shortcuts import redirect

import gameboard as gb


def get_game_variables():
    ret = {}
    ret['box1'] = gb.get_box_state(1)
    ret['box2'] = gb.get_box_state(2)
    ret['box3'] = gb.get_box_state(3)
    ret['box4'] = gb.get_box_state(4)
    ret['box5'] = gb.get_box_state(5)
    ret['box6'] = gb.get_box_state(6)
    ret['box7'] = gb.get_box_state(7)
    ret['box8'] = gb.get_box_state(8)
    ret['box9'] = gb.get_box_state(9)
    game_board = cache.get('ttt_game_board')
    ret['game_state'] = game_board.state
    ret['winner'] = game_board.winner

    return ret

#handles the "start game" view
def start_game(request):
    context = {}
    return render(request, 'game/startgame.html', context)

#handles when player presses "Start Game" button
def launch(request):
    game_board = gb.GameBoard(gb.PLAYER_X)
    game_board.computer_move()
    cache.set('ttt_game_board', game_board)

    context = get_game_variables()
    context = {'context': context}
    return redirect('game')

#loads the current game based on settings in memory
def game_page(request):
    context = get_game_variables()
    context = {'context': context}
    return render(request, 'game/game.html', context)

#handles user making a move
def ajax_make_move(request, box_choice):
    if request.is_ajax():
        game_board = cache.get('ttt_game_board')

        if game_board.state == gb.STATE_GAME_OVER:
            response = 'game-over'
        else:
            #turn count increases from player choosing move
            game_board.turn_count += 1
            #change game state to the computer
            game_board.state = game_board.side
            game_board.human_last_move = box_choice
            gb.try_set_box_state(box_choice, gb.opposing_player(game_board.side))
            move = game_board.computer_move()
            #save game_board
            cache.set('ttt_game_board', game_board)

            ret = get_game_variables()
            response = simplejson.dumps(ret)
    else:
        response = 'fail'

    return HttpResponse(response, mimetype="application/json")


