from annoying.decorators import ajax_request, render_to
from django.views.decorators.csrf import csrf_exempt
from .models import Game, Move
from .tictactoe import TicTacToe

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

        # Popoulate board that can be used with TicTacToe class
        board_values = board.split(',')
        board_dict = {}
        i = 0
        for x in range(3):
            for y in range(3):
                board_dict[x,y] = board_values[i] if board_values[i] != '' else None
                i += 1

        ttt = TicTacToe(board_dict, (move.x_position,move.y_position))
        next_move = ttt.minmax(False)
        if next_move['coordinates'] == None:
            coordinates = None
            state = "win" if next_move['value'] == -1 else "tie"
        else:
            state = None
            coordinates = {
                'x' : next_move['coordinates'][0],
                'y' : next_move['coordinates'][1],
            }

        return {
            'state' : state,
            'coordinates' : coordinates
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