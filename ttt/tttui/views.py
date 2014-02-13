import json

from django.core                  import serializers
from django.http                  import HttpResponse, HttpResponseRedirect
from django.shortcuts             import get_object_or_404, render_to_response
from django.template              import RequestContext
from django.views.decorators.http import require_GET, require_POST, \
                                         require_http_methods

from game.models import Game, PLAYER_O, PLAYER_X, PLAYER_NONE
from game.player import Computer

from random      import choice

@require_GET
def all(request):
    """
    List all games
    """
    games = Game.objects.all()
    return render_to_response(
        'index.html',
         {'games': games},
         context_instance=RequestContext(request))

@require_GET
def get(request, game_id):
    """
    Get a game
    """
    game = get_object_or_404(Game, pk=game_id)
    player = game.user_token
    return render_to_response(
        'game.html', 
        {
            'game':      game,
            'game_done': game.is_complete(),
            'player':    player,
            'PLAYER_X':  PLAYER_X,
            'PLAYER_O':  PLAYER_O,
        },
        context_instance=RequestContext(request))

