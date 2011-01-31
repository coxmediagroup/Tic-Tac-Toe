# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from DJTickyTack.models import Game, Move


def render_csrf(tpl, request, data):
    return render_to_response(tpl, data,
                              context_instance=RequestContext(request))



def index(request):
    return redirect(reverse(games))

@login_required
def games(request):
    if request.method == "POST":
        Game.createFor(request.user, request.POST.get('playAs', 'X'))
        return redirect(reverse(games))
    else:
        return render_csrf('games.html', request,
        {
            'activeGames': Game.findActiveFor(request.user),
            'pendingGames': Game.findPendingFor(request.user),
            'finishedGames': Game.findFinishedFor(request.user)
        })


@login_required # @TODO: maybe games should be public?
def game(request, gameId):
    game = Game.objects.get(pk=int(gameId))
    if request.method == "POST":

        # @TODO: encapsulate all this junk as method in Game
        t = game.asTicTacToe()
        m = request.POST.get('move')
        if m in t.moves and game.toPlay == request.user:
            move = Move(game=game, player=request.user, move=m)
            move.save()
            game.togglePlayer()
            state = getattr(t, m)
            if state.isOver:
                game.finished = True
                game.toPlay = None
                game.winner = (game.player1 if state.winner == 'X' else
                               game.player2 if state.winner == 'O' else
                               None)
            game.save()
            return redirect(reverse(games))
        else:
            return HttpResponseBadRequest('no.')
    else:
        return render_csrf('game.html', request,
        {
            'game' : game,
            'state' : game.asTicTacToe().currentState,
        })


@login_required
def joinable(request):
    # this is just a convienience for the pure HTML interface
    # @TODO: see if any browsers actually support url templates for forms
    if request.method == "POST":
        gameId = int(request.POST['gameId'])
        return join(request, gameId)
    else:
        return render_csrf('joinable.html', request,
        {
            'joinable': Game.findJoinableBy(request.user)
        })


@login_required
def join(request, gameId):
    # this is the nice restful interface
    if Game.tryToJoin(request.user, gameId):
        # @TODO: go directly to game if we're playing as X
        return redirect(reverse(games))
    else:
        return redirect(reverse(joinable))
