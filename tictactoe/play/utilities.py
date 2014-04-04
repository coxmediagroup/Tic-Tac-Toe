import json

from play.models import Game

def json_response(status, msg = None, move = None, game_state = None):
    from django.http import HttpResponse
    response = {"status": status}
    if msg is not None:
        response["msg"] = msg
    if move is not None:
        response["move"] = move
    if game_state is not None:
        response["state"] = game_state
    return HttpResponse(json.dumps(response))

# Create a new game in the database and set its ID in the session.
def new_game():
    game = Game()
    game.save()
    return game.id
