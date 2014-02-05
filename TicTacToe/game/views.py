from django.shortcuts import render
from django.http import HttpResponse
import simplejson
from django.core.cache import cache
from django.shortcuts import redirect

import gameboard as gb




#handles the "start game" view
def start_game(request):
    context = {}
    return render(request, 'game/startgame.html', context)

#handles when player presses "Start Game" button
def launch(request):
    game_board = gb.GameBoard(gb.PLAYER_O)
    #game_board.computer_move()
    cache.set('ttt_game_board', game_board)

    context = gb.get_game_variables(game_board)
    context = {'context': context}
    return redirect('game')

#loads the current game based on settings in memory
def game_page(request):
    context = gb.get_game_variables(gb.get_board())
    context = {'context': context}
    return render(request, 'game/game.html', context)

#handles user making a move
def ajax_make_move(request, box_choice):

    if request.is_ajax():
        game_board = gb.get_board()

        if game_board.state == gb.STATE_GAME_OVER:
            ret = gb.get_game_variables(game_board)
            response = simplejson.dumps(ret)
        else:
            #turn count increases from player choosing move
            game_board.turn_count += 1

            opposing_player = gb.opposing_player(game_board.side)

            #update board
            box_choice = int(box_choice)
            game_board.human_last_move = box_choice
            gb.try_set_box_state(box_choice,opposing_player)

            if gb.get_side_won(opposing_player):
                game_board.state = gb.STATE_GAME_OVER
                game_board.winner = opposing_player

            #check if last move filled the board (draw)
            elif gb.get_available_box() is None:
                game_board.state = gb.STATE_GAME_OVER
                game_board.winner = gb.DRAW
            else:
                #change game state to the computer
                game_board.state = game_board.side
                #get computer's move
                move = game_board.computer_move()
                #save game_board
                gb.save_board(game_board)

            ret = gb.get_game_variables(game_board)
            response = simplejson.dumps(ret)
    else:
        response = 'fail'

    return HttpResponse(response, mimetype="application/json")


