import json

from django.http import HttpResponse
from django.views.generic import TemplateView, View

from tic_tac_toe_play import get_next_opt_state, convert_repr
get_next_opt_state = convert_repr(get_next_opt_state)


class LoadTicTacToe(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):

        context = super(LoadTicTacToe, self).get_context_data(**kwargs)
        return context


class PlayTicTacToeAjax(View):
    play_func = staticmethod(get_next_opt_state)

    def get(self, request):
        current_state = request.GET.get('state')
        ai_player = request.GET.get('ai_player')
        next_state = PlayTicTacToeAjax.play_func(current_state,
                                                 ai_player)
        return HttpResponse(json.dumps({'state': next_state}),
                            mimetype="application/json")
