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
    if request.POST.get('play-as-o', False) is not False:
        game_board = gb.GameBoard(gb.PLAYER_X)
        game_board.computer_move()
    else:
        game_board = gb.GameBoard(gb.PLAYER_O)

    game_board.save()

    return redirect('game')

#loads the current game based on settings in memory
def game_page(request):
    context = gb.GameBoard.get().get_game_variables()
    context = {'context': context}
    return render(request, 'game/game.html', context)

#handles user making a move
def ajax_make_move(request, box_choice):

    if request.is_ajax():
        game_board = gb.GameBoard.get()

        if game_board.check_game_over() is False:

            #update board
            game_board.human_move(box_choice)

            #check if last move filled the board (draw)
            if game_board.check_game_over() is False:
                #change game state to the computer
                game_board.set_turn(game_board.side)
                #get computer's move
                game_board.computer_move()
                #check if game is over
                game_board.check_game_over()

            game_board.save()
            ret = game_board.get_game_variables()
            response = simplejson.dumps(ret)
    else:
        response = 'fail'

    return HttpResponse(response, mimetype="application/json")


