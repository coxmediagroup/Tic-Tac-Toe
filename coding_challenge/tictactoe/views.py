import json

from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateView

from tic_tac_toe_play import get_next_state

from django.conf import settings
D = settings.D


class LoadTicTacToe(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):

        context = super(LoadTicTacToe, self).get_context_data(**kwargs)
        return context


class PlayTicTacToeAjax(View):
    def get(self, request):
        current_state = request.GET.get('state')
        ai_player = request.GET.get('ai_player')
        next_state = get_next_play(
            current_state,
            ai_player,
            get_next_state)
        return HttpResponse(json.dumps({'state': next_state}),
                            mimetype="application/json")


def get_next_play(current_state, player, play_func):
    current_state = str(current_state)
    player = str(player)
    from_str = lambda state: [list(state[i:i+3]) for i in (0, 3, 6)]
    to_str = lambda state: ''.join([''.join(r) for r in state])
    return to_str(play_func(from_str(current_state), player))
