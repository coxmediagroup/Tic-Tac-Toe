# -*- coding: utf-8 -*-

import logging

from django.http import HttpResponse
from django.template import RequestContext
from lazysignup.decorators import allow_lazy_user
from django.shortcuts import render_to_response, get_object_or_404

from game.models import Game

log = logging.getLogger('game.views')

@allow_lazy_user
def index(request, cell=None, template_name='game/index.html'):
    '''
    Display current game being played.

    **Arguments**

    ``template_name``
      A custom template to use. This is optional.
    '''
    # Normally I wouldn't store games in session like this, but I
    # think it works well with my goal of making games as transparent
    # as possible to the user (no sign-in, can leave and come
    # back to continue game where it was left off, etc.)
    game = request.session.get('game', None)
    if game is None:
        game = Game(player=request.user)
        request.session['game'] = game
    games = Game.objects.filter(player=request.user)
    return render_to_response(template_name, {
        'cell': game.board,
        'played': games.count(),
        'won': games.filter(status=Game.WON).count(),
        'tied': games.filter(status=Game.TIE).count(),
        'lost': games.filter(status=Game.LOST).count(),
    }, context_instance=RequestContext(request))
