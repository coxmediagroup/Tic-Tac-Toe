from django.http import HttpResponse
from annoying.decorators import render_to
from core.models import Game

@render_to('core/core.html')
def main(request):
    new_game = Game.objects.create()
    return {'game_num': new_game.id}


@render_to('core/board.html')
def player_move(request, game_id, space_id):
    return HttpResponse("True")


def calculate_computer_move(request, current_game):
    pass


def computer_move(request):
    pass
