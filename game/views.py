# -*- coding: utf-8 -*-

import logging

from django.http import HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from lazysignup.decorators import allow_lazy_user
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse

from game.models import Game

log = logging.getLogger('game.views')

@allow_lazy_user
def new_X(request):
    '''Start a new game, with human player being 'X' (plays first)'''
    game = Game(player=request.user, symbol='X')
    game.board = [' ',] * 9
    game.save()
    # Store game id in session memory as 'current' game
    request.session['game_id'] = game.id
    return HttpResponseRedirect(reverse('game:index'))

@allow_lazy_user
def new_O(request):
    '''Start a new game, with human player being 'O' (plays second)'''
    game = Game(player=request.user, symbol='O')
    # Computer player always starts upper left corner when X
    game.board = [' ',] * 9
    game.board[0] = 'X'
    game.save()
    # Store game id in session memory as 'current' game
    request.session['game_id'] = game.id
    return HttpResponseRedirect(reverse('game:index'))

@allow_lazy_user
def index(request, template_name='game/index.html'):
    '''
    Display current game being played.

    **Arguments**

    ``template_name``
      A custom template to use. This is optional.
    '''

    # Check if a cell was clicked
    cell = request.GET.get('cell', None)
    if cell is not None:
        try:
            cell = int(cell)
        except ValueError:
            cell = None
        finally:
            if not 0 <= cell <= 8:
                # Bad cell parameter.. should be between 0 and 8
                cell = None

    # Get 'current' game pk from session storage and then game from database
    game_id = request.session.get('game_id', None)
    if game_id is None:
        game = None
    else:
        try:
            game = Game.objects.get(pk=game_id)
        except game.DoesNotExist:
            game = None

    # Was a cell clicked and passed in as param in URL?
    if cell is None:
        if game is None:
            # Don't create a game if no cell clicked
            board = '         '
        else:
            # Just redraw current game board
            board = game.board
        # TODO: add alert message?
    else:
        if game is None:
            # Player clicked square but no game, so let's create one now
            game = Game(player=request.user, symbol='X')
            game.board = [' ',] * 9

        # Verify this is valid location to play (ignore it if it isn't)
        if game.board[cell] == ' ':
            game.board[cell] = game.symbol
            # Generate computer move
            game.machine_move()

        game.save()
        request.session['game_id'] = game.id
        board = game.board

    games = Game.objects.filter(player=request.user)
    return render_to_response(template_name, {
        'cell': board,
        'played': games.count(),
        'won': games.filter(status=Game.WON).count(),
        'tied': games.filter(status=Game.TIE).count(),
        'lost': games.filter(status=Game.LOST).count(),
    }, context_instance=RequestContext(request))
