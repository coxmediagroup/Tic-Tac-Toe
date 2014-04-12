from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext

from game.forms import GameForm

def play(request):
    context = {}

    form = GameForm(request.POST or None)
    context['form'] = form
    return render_to_response('game/play.html',
                              context,
                              context_instance=RequestContext(request))
