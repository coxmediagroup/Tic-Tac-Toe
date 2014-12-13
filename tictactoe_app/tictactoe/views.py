from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import uuid

from tictactoe.models import PersistentGameState

# Create your views here.

def index(http_request):
  context = {"gameIds":PersistentGameState.getAllGameIds()}
  return render(http_request, 'index.html', context)

def success_response(game, **kw):
  body = {"status":"success", "game":game.summarize()}
  body.update(kw)
  return JsonResponse(body)

from pprint import pprint as pp
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def game(request, game_id=None):
  if not game_id:
    game_id = str(uuid.uuid4())
  g = PersistentGameState.load(game_id)
  if 'player' not in request.POST.keys():
    return success_response(g)
  else:
    player = request.POST['player']
    position = int(request.POST['position'])
    valid, data = g.validate_next(player, position)
    if not valid:
      return JsonResponse({"status":"error", "message":data})
    else:
      g.save_move(*data)
      if g.isFinished():
        return success_response(g)
      else:
        return do_computer_move(player, g)


def do_computer_move(last_player, game):
  computer_player = 'O' if last_player == 'X' else 'X'
  winSurety, computer_move = game.suggest_next(computer_player)
  valid, data = game.validate_next(computer_player, computer_move)
  if not valid:
    # malfunctioning minmax
    raise Exception("Computer player tried to play an invalid move")
  else:
    game.save_move(*data)
    return success_response(game)

