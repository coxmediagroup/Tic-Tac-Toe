from django.views.generic import TemplateView
from django.contrib.sites.models import Site
import json


class GameView(TemplateView):
    template_name = 'tictactoe/gameview.html'
    def get_context_data(self, **kwargs):
        ctx = super(GameView, self).get_context_data(**kwargs)

        if 'game_so_far' in kwargs:
            ctx['game_so_far'] = json.dumps(kwargs['game_so_far'].split('-'))
            ctx['player'] = json.dumps(kwargs['player'])

        print dir(Site.objects)
        ctx['current_site'] = json.dumps(Site.objects.get_current().domain)

        return ctx

game_view = GameView.as_view()
