from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext

from game.forms import GameForm
from localcore.utils import MoveGenerator

def play(request):
    context = {}

    form = GameForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            mgen = MoveGenerator(form.cleaned_data)

            if request.is_ajax():
                context['form'] = form
                return render_to_response('game/game_template.html',
                                          context,
                                          context_instance=RequestContext(request))
        else:
            f = forms.errors
            raise Exception
            form = GameForm()

    context['form'] = form
    return render_to_response('game/play.html',
                              context,
                              context_instance=RequestContext(request))
