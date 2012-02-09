# -*- coding: utf-8 -*-

import logging

from django.http import HttpResponse
from django.template import RequestContext
from lazysignup.decorators import allow_lazy_user
from django.shortcuts import render_to_response, get_object_or_404

from game.models import Game

@allow_lazy_user
def index(request, template_name='game/index.html'):
    '''
    Display current game being played.

    **Arguments**

    ``template_name``
      A custom template to use. This is optional.
    '''
    games = Game.objects.filter(user=request.user)
    return render_to_response(template_name, {
        'played': games.count(),
        'won': games.filter(status=Game.WON).count(),
        'tied': games.filter(status=Game.TIE).count(),
        'lost': games.filter(status=Game.LOST).count(),
    }, context_instance=RequestContext(request))
