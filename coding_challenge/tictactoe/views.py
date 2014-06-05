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
        current_player = request.GET.get('player')
        next_state = get_next_state(current_state, current_player)
        return HttpResponse(json.dumps(next_state),
                            mimetype="application/json")
