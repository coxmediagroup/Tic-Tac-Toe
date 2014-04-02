from django.http import HttpResponse
from annoying.decorators import render_to
from core.models import Game, Move

@render_to('core/core.html')
def main(request):
    new_game = Game.objects.create()
    return {'game_num': new_game.id}


@render_to('core/board.html')
def player_move(request, game_id, space_id):
    # take space_id and create a move object
    # then call calculate_computer_move
    # then make the move by calling computer_move
    # then return the new board

    current_game = Game.objects.get(id=game_id)
    new_player_move = Move.objects.create(game=current_game, space=space_id)

    calculate_computer_move(request, current_game)

    return HttpResponse("True")


def calculate_computer_move(request, current_game):
    # this is where we'll store the rules for the game
    pass


def computer_move(request):
    # create a move object with space_id from calculate_computer_move
    # return all the info needed to redraw the board
    pass
