# Create your views here.
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from DJTickyTack.models import Game

def index(request):
    return render_to_response('index.html')

@login_required
def games(request):
    if request.method == "POST":
        Game.createFor(request.user, request.POST.get('playAs', 'X'))
        return redirect(reverse(games))
    else:
        return render_to_response('games.html',
        {
            'activeGames': Game.findActiveFor(request.user),
            'pendingGames': Game.findPendingFor(request.user)
        })


def joinable(request):
    return render_to_response('joinable.html',
    {
        'joinable': Game.findJoinableBy(request.user)
    })


@login_required
def join(request):
    raise hell
