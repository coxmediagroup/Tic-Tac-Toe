from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
import uuid
from pprint import pprint as pp
from django.views.decorators.csrf import csrf_exempt

from tictactoe_api.models import PersistentGameState


def success_response(game, **kw):
  "standard format successful API response"
  body = {"status":"success", "game":game.summarize()}
  body.update(kw)
  return JsonResponse(body)

def error_response(message, status=400):
  "standard format unsuccessful API response. Set appropriate status if it's your error and not user input"
  return JsonResponse({"status":"error", "message":message}, status=status)

def computer_misplay_response(reason):
  "response for plugging into execute_move that explains the reason"
  return error_response("Move tallied, but Computer followed with an invalid move: %s"%(reason,), status=500)
    


def list_games(request):
  "return all the games for which there's been a recorded move"
  gameIds = list(PersistentGameState.getAllGameIds())
  return JsonResponse({'status':'success', 'gameIds':gameIds})



@csrf_exempt
def new_game(request):
  "synthesize a new ID and redirect to it. The returned ID is ephemeral until a move is posted"
  if request.method != 'POST':
    return error_response("Must POST to get a new game ID")
  else:
    game_id = str(uuid.uuid4()) # TODO move ID synthesis to the model
    return redirect('get_game', game_id=game_id)



def get_game(request, game_id):
  g = PersistentGameState.load(game_id)
  return success_response(g)



@csrf_exempt
def make_move(request, game_id):
  g = PersistentGameState.load(game_id)
  player = request.POST['player']
  position = int(request.POST['position'])
  return g.execute_move(
    player,
    position,
    onValid = do_computer_move,
    onInvalid = error_response
    )


def do_computer_move(game):
  if game.isFinished():
    return success_response(game)
  else:
    computer_player = 'O' if game.last_player() == 'X' else 'X'
    _, computer_move = game.suggest_next(computer_player)
    return game.execute_move(
      computer_player,
      computer_move,
      onValid = success_response,
      onInvalid = computer_misplay_response
      )



