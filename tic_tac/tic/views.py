import json
import urllib
import random


from django.http import HttpResponse
from django.template import RequestContext, loader


from tic.models import GameBoard, GameSquare

def index(request):
    return HttpResponse("Hello - GAME ON")

def new_game(request):
    #return HttpResponse("JSON resource - new board")
    board = GameBoard.objects.create()
    board.square11 = GameSquare.objects.create()
    board.square12 = GameSquare.objects.create()
    board.square13 = GameSquare.objects.create()
    board.square21 = GameSquare.objects.create()
    board.square22 = GameSquare.objects.create()
    board.square23 = GameSquare.objects.create()
    board.square31 = GameSquare.objects.create()
    board.square32 = GameSquare.objects.create()
    board.square33 = GameSquare.objects.create()
    # Give the AI a 50/50 chance to go first
    if random.randint(1,2) % 2 == 0:
       board.AI_move() 
    board.save()
    display = "{}\n{}".format(board.simple_display(), str(board))
    return HttpResponse(display, content_type="application/json")

def player_move(request):
    board_id = request.GET["id"]
    board = GameBoard.objects.get(id=board_id)

    data = request.GET["board"]
    data = urllib.unquote(data).decode('utf8')

    try:
        new_board = json.loads(data)
    except ValueError, e:
        return HttpResponse("ERROR: {} for {}".format(e, data))

    if type(new_board) != type({}) or \
        '11' not in new_board or \
        '12' not in new_board or \
        '13' not in new_board or \
        '21' not in new_board or \
        '22' not in new_board or \
        '23' not in new_board or \
        '31' not in new_board or \
        '32' not in new_board or \
        '33' not in new_board:
        return HttpResponse("ERROR: Malformed game board, {}".format(new_board))

    board.update(new_board)

    # for this demo, let player be x always
    if board.game_won('x'):
        return HttpResponse("Congrats!  You win!<hr>{}".format(board))

    board.AI_move()
    if board.game_won('o'):
        return HttpResponse("Shame!  The AI won!<hr>{}".format(board))

    display = "{}\n{}".format(board.simple_display(), str(board))
    return HttpResponse(display, content_type="application/json")
