from django.views.generic import TemplateView
from django.contrib.sites.models import Site
from django.http import HttpResponse


import json

from . import models

class GameView(TemplateView):
    template_name = 'tictactoe/gameview.html'


    def get_ip(self):
        return (self.request.META.get('HTTP_X_FORWARDED_FOR') 
                or self.request.META.get('REMOTE_ADDR') 
                or '127.0.0.1')


    def get_context_data(self, **kwargs):
        ctx = super(GameView, self).get_context_data(**kwargs)

        if 'game_so_far' in kwargs:
            ctx['game_so_far'] = json.dumps(kwargs['game_so_far'].split('-'))
            ctx['player'] = json.dumps(kwargs['player'])

        print dir(Site.objects)
        ctx['current_site'] = json.dumps(Site.objects.get_current().domain)

        return ctx

    def post(self, request, *args, **kwargs):
        game = {}

        pk = request.session.get('tictactoe_id')
        gmodel = models.Game.create_or_append(pk, self.get_ip(), kwargs['player'], kwargs['game_so_far'])
        request.session['tictactoe_id'] = pk = gmodel.id

        if gmodel.winner:
            del request.session['tictactoe_id']

        return HttpResponse(json.dumps({'pk':pk, 'winner':gmodel.winner}),
            content_type="application/json")

game_view = GameView.as_view()
