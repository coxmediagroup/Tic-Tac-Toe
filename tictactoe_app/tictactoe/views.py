from django.shortcuts import render
from django.http import HttpResponse
import json
import uuid

from tictactoe.models import PersistentGameState

# Create your views here.

def index(http_request):
  return HttpResponse("hello there")

def success_response(game, **kw):
  body = {"status":"success", "game":game.summarize()}
  body.update(kw)
  return HttpResponse(json.dumps(body), content_type="application/json")

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
      return {"status":"error", "message":data}
    else:
      g.save_move(*data)
      if g.isWon():
        return success_response(g, yourWin=True)
      else:
        return do_computer_move(player, g)


def do_computer_move(last_player, game):
  computer_player = 'O' if player == 'X' else 'X'
  winSurety, computer_move = g.suggest_next(computer_player)
  valid, data = g.validate_next(computer_player, computer_move)
  if not valid:
    # malfunctioning minmax
    raise Exception("Computer player tried to play an invalid move")
  else:
    g.save_move(*data)
    if g.isWon():
      return success_response(g, yourWin=False)
    return success_reponse(g)



