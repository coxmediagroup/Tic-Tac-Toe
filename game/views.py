from django.core                  import serializers
from django.core.urlresolvers     import reverse
from django.http                  import HttpResponse, HttpResponseRedirect
from django.shortcuts             import get_object_or_404, render_to_response
from django.template              import RequestContext
from django.utils                 import simplejson
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
    return render_to_response('index.html', {'games':games}, context_instance=RequestContext(request))

@require_GET
def get(request, game_id):
    """
    Get a game
    """
    game = get_object_or_404(Game, pk=game_id)
    player = 'x' if game.is_user_x else 'o'
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

@require_POST
def new(request):
    """
    Create a new game and redirect to it
    """
    game = Game.create_new(is_user_x=choice([True,False]))
    if game.is_user_x == False:
        game[1][1] = PLAYER_X # computer goes to the middle 
    return HttpResponseRedirect(reverse('game.views.get', args=(game.id,)))

@require_POST
def move(request, game_id):
    """
    Post a move to a game
    """

    # place holders for response
    game = get_object_or_404(Game, pk=game_id)
    player = None
    comp   = None
    move   = None

    if not game.is_complete():
        # make sure we have the needed values
        assert 'player' in request.POST and 'col' in request.POST and 'row' in request.POST

        # make sure the user is making a move
        assert (game.is_user_x and request.POST['player'] == 'x') or \
               (not game.is_user_x and request.POST['player'] == 'o') 
        player = PLAYER_X if game.is_user_x else PLAYER_O

        assert game.who_moves() == player

        # make user move
        game[int(request.POST['col'])][int(request.POST['row'])] = player

        # make computer move
        comp = game.who_moves()
        if comp != PLAYER_NONE:
            move = Computer.determine_move(game, comp, player)
            game[move[0]][move[1]] = comp
    
    if request.is_ajax():
        # Since this is an ajax call, we only need to send data
        # about overall game state and the computer's last move, if any
        winner = game.who_won()
        winner = 'x' if winner == PLAYER_X else 'o' if winner == PLAYER_O else '-'
        comp   = 'x' if comp == PLAYER_X else 'o' if comp == PLAYER_O else '-'
        return HttpResponse(
            simplejson.dumps( 
                {
                'player': comp,
                'col':move[0] if move is not None else '',
                'row':move[1] if move is not None else '',
                'is_complete': game.is_complete(),
                'winner': winner,
                }),
            'application/javascript')
    else:
        return HttpResponseRedirect(reverse('game.views.get', args=(game.id,)))

