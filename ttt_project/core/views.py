import random
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
    all_spaces = [0,1,2,3,4,5,6,7,8]

    # get all moves for this game
    moves_for_current_game = Move.objects.filter(game=current_game)

    # If it's the first move of the game, just pick a random space
    if moves_for_current_game.count() == 1:
        player_space = moves_for_current_game[0].space
        all_spaces.remove(player_space)

        # pick one of the remaining spaces
        space_for_computer_move = random.choice(all_spaces)
        new_computer_move = Move.objects.create(game=current_game, player_move=False, space=space_for_computer_move)

        return

    else:
        # need to figure out if player has 2 moves that could equal a win
            # if so, computer move blocks it
            # if not, check if computer has 2 moves that could equal a win
                # if so, play to win
                # if not, play to add a second move that could equal a win
        pass


def computer_move(request):
    # create a move object with space_id from calculate_computer_move
    # return all the info needed to redraw the board
    pass
