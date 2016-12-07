from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.conf import settings
from django.template import RequestContext

from game.forms import GameForm
from localcore.utils import MoveGenerator

def play(request):
    context = {}

    form = GameForm(request.POST or None)

    if request.method == 'POST' or request.GET.get('goSecond') or request.GET.get('goFirst'):
        d = {}
        mgen = None
        if request.method == 'POST' and form.is_valid():
            mgen = MoveGenerator(form.cleaned_data)
        elif request.GET.get('goSecond'):
            mgen = MoveGenerator({})
        
        if mgen:
            mgen.make_move()
            d = mgen.box_dict()
            context['first'] = mgen.first
            context['second'] = mgen.second
            if mgen.winner:
                if mgen.winner == '1':
                    context['winner'] = 'Lost'
                elif mgen.winner == '2':
                    context['winner'] = 'Won'
                else:
                    context['winner'] = 'Drew'
                context['winning_three'] = mgen.winning_three

        form = GameForm(d or None)
        if request.is_ajax():
            context['form'] = form
            return render_to_response('game/game_template.html',
                                      context,
                                      context_instance=RequestContext(request))
        else:
            context['board'] = render_to_string('game/game_template.html',{'form':form})

    context['form'] = form
    return render_to_response('game/play.html',
                              context,
                              context_instance=RequestContext(request))
