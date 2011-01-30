# Create your views here.
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.template.context import RequestContext
from DJTickyTack.models import Game


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
            'pendingGames': Game.findPendingFor(request.user)
        })


@login_required # @TODO: maybe games should be public?
def game(request, gameId):
    if request.method == "POST":
        pass # @TODO: post new move
    else:
        return render_csrf('game.html', request,
        {
            'game' : Game.objects.get(pk=int(gameId))
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
