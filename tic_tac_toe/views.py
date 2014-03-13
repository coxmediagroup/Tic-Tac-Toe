from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

import tic_tac_toe.util as util

# Create your views here.

def index(request):
    game = util.get_game(request)  # get the game object from the session

    # check for a winner
    winner = game.get_winner()

    # is it the computer's turn?
    current_player = game.current_player == 1 and game.player_one or game.player_two
    if not winner and current_player.is_ai:  # Don't bother if someone has won
        # if so, he should go on and take his turn
        current_player.get_decision()
        winner = game.get_winner()  # the board has changed, check for a winner

    # now, it's our turn
    ### display the board
    board = game.board_set.first()  # get the board
    rows = board.row_set.all()  # get the board's rows

    locations = []  # this will hold each cell and its contents
    for row_i, row in enumerate(rows):
        row_locations_set = row.location_set.all()
        row_locations = []  # this will be our translated row
        for loc_i, location in enumerate(row_locations_set):
            # figure out who owns the cell
            symbol = ''  # default to unowned
            if location.occupier is not None:
                symbol = location.occupier.symbol

            location_tpl = (row_i, loc_i, symbol)
            row_locations.append(location_tpl)  # add the location to the row
        locations.append(row_locations)  # add the row to the board

    # invert the grid vertically so we can build from the top down
    locations = locations[::-1]

    # and let's get some input

    context = {'board':locations, 'winner':winner}
    return render(request, 'board.html', context)

def make_move(request, row_id, column_id):
    # check that the requested location is valid
    # row id and column id should be numbers between 0 and 2 inclusive
    row_valid = row_id.isdigit() and int(row_id) in range(3)
    column_valid = column_id.isdigit() and int(column_id) in range(3)

    if row_valid and column_valid:
        game = util.get_game(request)  # get game from session

        player = util.get_human_player(game)  # get human player from game
        location = game.get_location(row_id, column_id)  # get Location object
        location.claim(player)  # claim the location for the player
        location.save()

        game.next_player()

    return redirect('tic_tac_toe.views.index')

def reset(request):
    # abandon any games that may currently be in the session
    request.session['game_id'] = None

    # redirect to index
    return redirect('tic_tac_toe.views.index')

