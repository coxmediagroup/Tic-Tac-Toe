
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from tictac.constants import SYMBOL_CHOICES
from tictac.forms import NewGameForm, PlayForm
from tictac.models import Game

def welcome(request):
    """
    Main entry for our game.
    """

    initial={'player1_auto':False, 'player1_symbol': '0',
             'player2_auto':True, 'player2':'Joshua', 'player2_symbol' : '1'}
    game_id = request.session.get('game_id')
    try:
        if game_id:
            game = Game.objects.get(id=game_id)
            game_players = game.gameplayers_set.all()

            initial = {
                'player1':game_players[0].player.first_name,
                'player1_auto':game_players[0].player.auto,
                'player1_symbol':game_players[0].symbol,
                'player2':game_players[1].player.first_name,
                'player2_auto':game_players[1].player.auto,
                'player2_symbol':game_players[1].symbol,
            }
    except:
        pass

    new_game_form = NewGameForm(initial=initial)

    return render(request, 'welcome.html', {
        'form': new_game_form,
        'symbol_choices' : SYMBOL_CHOICES,
        })

def new_game(request):
    """
    Create a new game or at least zap the existing one.
    """
    if request.POST:

        form = NewGameForm(request.POST)
        if form.is_valid():
            game = Game.objects.new_game(game_type=form.cleaned_data['game_type'],
                players=[
                    { 'name' : form.cleaned_data['player1'],
                      'auto': form.cleaned_data['player1_auto'],
                      'symbol' : form.cleaned_data['player1_symbol'] },
                    { 'name' : form.cleaned_data['player2'],
                      'auto': form.cleaned_data['player2_auto'],
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

    game = Game.objects.filter(id=game_id).first()

    if game:
        players = [
            {'name':p['first_name'], 'number':p['gameplayers__number'],
                'symbol':p['gameplayers__symbol'],
                'auto':p['auto'], }

            for p in game.players.values('first_name',
                'gameplayers__number','gameplayers__symbol',
                'auto').order_by('gameplayers__number')]

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
        # Bogus defaults for non-playing game.
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
    """
    Make our play.
    """
    if request.POST:
        game_id = request.session.get('game_id')
        if game_id is not None:
            game = Game.objects.get(id=request.session['game_id'])

        if game:

            form = PlayForm(request.POST)
            if form.is_valid():
                player = form.cleaned_data['player']
                position = form.cleaned_data['position']
                game.play_turn(player, position=position)

            response_json = json.dumps({'ok' : True})
            return HttpResponse(response_json, content_type='application/json')

    return redirect(reverse('tictac_game_board'))

