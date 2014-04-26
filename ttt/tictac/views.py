
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from tictac.models import Game
from tictac.forms import NewGameForm, PlayForm

# Create your views here.

def welcome(request):

    new_game_form = NewGameForm(initial={'player1_auto':'person',
        'player2_auto':'computer', 'player2':'Joshua'})

    return render(request, 'welcome.html', {
        'form': new_game_form,
        })

def new_game(request):
    if request.POST:

        form = NewGameForm(request.POST)
        if form.is_valid():
            game = Game.objects.new_game(game_type=form.cleaned_data['game_type'],
                players=[
                    { 'name' : form.cleaned_data['player1'], 'auto': form.cleaned_data['player1_auto'],
                        'symbol' : form.cleaned_data['player1_symbol'] },
                    { 'name' : form.cleaned_data['player2'], 'auto': form.cleaned_data['player2_auto'],
                        'symbol' : form.cleaned_data['player2_symbol'] },
                ])
            game.save()

            request.session['game_id'] = game.id
    else:
        request.session['game_id'] = None

    return redirect(reverse('tictac_welcome'))

def game_board(request, game_id=None):
    """
    Fetch either a specific board OR the one for the current session, if
    not specified.
    """

    if game_id is None:
        game_id = request.session.get('game_id')

    game = Game.objects.filter(id=request.session['game_id']).first()

    if game:
        players = [
            {'name':p['first_name'], 'number':p['gameplayers__number'],
                'avatar':p['avatar'], 'symbol':p['gameplayers__symbol'],}

            for p in game.players.values('first_name',
                'gameplayers__number','avatar','gameplayers__symbol').order_by('gameplayers__number')]

        game_resp = {
            'playing' : True,
            'state' : game.board.state,
            'rows' : game.board.rows,
            'columns' : game.board.columns,
            'has_winner' : game.has_winning_board(),
            'game_over' : game.game_over,
            'players' : players,
            'next_player': game.next_gameplayer().number,
            'turn_counter': game.turn_counter,
        }
    else:
        game_resp = {
            'playing' : False,
            'state' : ' '*9,
            'rows' : 3,
            'columns' : 3,
            'has_winner' : False,
            'game_over' : False,
            'players' : [],
            'next_player': None,
            'turn_counter': 0,
        }

    game_json = json.dumps(game_resp)
    return HttpResponse(game_json, content_type='application/json')

@csrf_exempt
def make_play(request):

    if request.POST:
        game_id = request.session.get('game_id')
        if game_id is not None:
            game = Game.objects.get(id=request.session['game_id'])

        if game:

            form = PlayForm(request.POST)
            if form.is_valid():
                player = form.cleaned_data['player']
                position = form.cleaned_data['position']
                game.play_turn(player, position)

            response_json = json.dumps({'ok' : True})
            return HttpResponse(response_json, content_type='application/json')

    import pdb; pdb.set_trace()
    return redirect(reverse('tictac_game_board'))

