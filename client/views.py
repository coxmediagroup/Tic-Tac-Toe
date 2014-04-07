from annoying.decorators import ajax_request, render_to
from django.views.decorators.csrf import csrf_exempt
from .models import Game, Move


@render_to('client/home.html')
def home(request):
    return {}

@csrf_exempt
@ajax_request
def make_move(request):
    board = request.POST.get('board', None)
    game = request.POST.get('game', None)
    x = request.POST.get('x', None)
    y = request.POST.get('y', None)

    if board and game and x and y:

        move = Move()
        move.board = board
        move.game = Game.objects.get(pk=game)
        move.x_position = int(x)
        move.y_position = int(y)
        move.save()

        return {
            'x' : 1,
            'y' : 2,
        }
    else:
        return {
            'error' : 'You are missing a required parameter.'
        }


@csrf_exempt
@ajax_request
def new_game(request):
    name = request.POST.get('name', None)
    if name:
        game = Game(name=name)
        game.save()
        result = {
            'id' : game.id
        }
    else:
        result = {
            'error' : "'name' field is required."
        }

    return result