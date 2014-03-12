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

    board = game.board_set.first() # get the board
    rows = board.row_set.all() # get the board's rows

    locations = [] # this will hold each cell and its contents
    for row_i, row in enumerate(rows):
        row_locations_set = row.location_set.all()
        row_locations = [] # this will be our translated row
        for loc_i, location in enumerate(row_locations_set):
            # figure out who owns the cell
            symbol = '' # default to unowned
            if(location.occupier != None):
                symbol = location.occupier.symbol

            location_tpl = (row_i, loc_i, symbol)
            row_locations.append(location_tpl) # add the location to the row
        locations.append(row_locations) # add the row to the board

    # invert the grid vertically so we can build from the top down
    locations = locations[::-1]

    # DEBUG: show locations, so it can be verified
    import pprint
    rendered_html = pprint.pformat(locations)

    # and let's get some input

    return HttpResponse(rendered_html)

def make_move(request, row_id, column_id):
    return HttpResponse('Move')
