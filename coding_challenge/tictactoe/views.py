import json

from django.http import HttpResponse
from django.views.generic import TemplateView, View

from tic_tac_toe_play import get_next_opt_state as play_func


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
            ai_player)
        return HttpResponse(json.dumps({'state': next_state}),
                            mimetype="application/json")


def get_next_play(current_state, player):
    from_str = lambda state: [list(state[i:i+3]) for i in (0, 3, 6)]
    to_str = lambda state: ''.join([''.join(r) for r in state])

    current_state = str(current_state)
    if current_state:
        current_state = from_str(current_state)
    player = str(player)

    next_state = play_func(current_state, player)
    return to_str(next_state)
