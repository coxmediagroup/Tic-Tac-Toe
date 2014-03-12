from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from tic_tac_toe.models import Game

# Create your views here.

def index(request):
    session = request.session # go on and grab the session so we only
                              #     incur this overhead once

    # get our game
    game_id = session.get('game_id')

    if game_id != None: # if we found a game id in the session
        try:
            # try to load the game in the session
            game = Game.objects.get(pk=game_id)
        except ObjectDoesNotExist:
            # if we can't load it, pretend we never saw the id
            game_id = None

    if game_id == None:
        # if we don't have a game yet, create one and store it
        game = Game()
        game.setup_new_game()
        session['game_id'] = game.id

    # is it the computer's turn?
        # if so, he should go on and take his turn

    # it's our turn, so:
    # display the board
    # and let's get some input

    return HttpResponse('Index')

def make_move(request, row_id, column_id):
    return HttpResponse('Move')
