from django.shortcuts import render
from django.http import HttpResponse
import json

from tictactoe.models import PersistentGameState

# Create your views here.

def index(http_request):
  return HttpResponse("hello there")

def success_response(game, **kw):
  body = {"status":"success", "game":game.summarize()}
  body.update(kw)
  return HttpResponse(json.dumps(body), content_type="application/json")

def get_game(request, game_id=None):
  if not game_id:
    game_id = str(uuid.uuid4())
  g = PersistentGameState.hydrate(game_id)
  return success_response(g)

def computer_move(last_player, game):
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
  
def try_move(request, game_id, player, position):
  g = PersistentGameState.hydrate(game_id)
  valid, data = g.validate_next(player, position)
  if not valid:
    return {"status":"error", "message":data}
  else:
    g.save_move(*data)
    if g.isWon():
      return success_response(g, yourWin=True)
    else:
      return computer_move(player, g)
      




