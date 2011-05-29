from logic import Game, Board, Player, Computer
import pickle
from functools import wraps
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
import forms
from django.core.urlresolvers import reverse
from django.utils import simplejson as sj

def get_game(f):
    """
    Gets the board data from the session and auto-appends it to the argument list 
    of the view
    """
    @wraps(f)
    def newf(request, *args, **kwargs):
        if request.session.get('game', None):
            game = request.session['game']
        else:
            return HttpResponseRedirect('/')
        kwargs['game'] = game
        return f(request, *args, **kwargs)
    return newf
        
def index(request):
    """
    New game form main page
    """
    f = forms.NewGameForm()
    return render_to_response('new_game_form.html', dict(form=f))

def new_game(request):
    """
    Creates a new game with the player or computer first, makes the first 
    move if the computer is first, and redirect to the board page.
    """
    if request.method != 'POST':
        return HttpResponseRedirect(reverse(index))

    f = forms.NewGameForm(request.POST)
    if not f.is_valid():
        return HttpResponse('<h1>Error in form post.</h1> %s'%f)
    player_first = f.cleaned_data['player_first']
    if player_first:
        game = Game(Board(), Player, Computer) 
        game.player_id = 1
    else:
        game = Game(Board(), Computer, Player)
        game.set_move()
        game.player_id = 2

    request.session['game'] = game
    return HttpResponseRedirect(reverse(render_board))

@get_game
def render_board(request, game):
    f = forms.NewGameForm()
    avatar = 'X' if game.player_id == 1 else 'O'
    return render_to_response('base.html', dict(game=game, form=f, avatar=avatar))

@get_game
def set_move(request, game):
    f = forms.MoveForm(request.POST)
    if not f.is_valid():
        return HttpResponse(sj.dumps(dict(condition='error',
                                          message='Error validating post data.')))
    move = (f.cleaned_data['x'], f.cleaned_data['y'])
    if move not in game.board.get_valid_moves():
        return HttpResponse(sj.dumps(dict(condition='error',
                                          message='Move is not a valid move')))
    con = game.set_move((f.cleaned_data['x'], f.cleaned_data['y']))
    if con['condition']:
        request.session['game'] = game
        return HttpResponse(sj.dumps(con))

    con = game.set_move()
    request.session['game'] = game
    return HttpResponse(sj.dumps(con))
