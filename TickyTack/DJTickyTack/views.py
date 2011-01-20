# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from DJTickyTack.models import Game

def index(request):
    return render_to_response('index.html')

@login_required
def home(request):
    return render_to_response('home.html',
    {
        'activeGames': Game.findAllFor(request.user)
    })
