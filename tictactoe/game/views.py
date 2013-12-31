from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from game.models import *
import json

class Index(TemplateView):
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        object = SingleGame(pk = 1)
        object.save()
        return super(Index, self).get(*args, **kwargs)

class PlayGame(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(PlayGame, self).dispatch(*args, **kwargs)

    def post(self, request, pk = 1, *args, **kwargs):
        game = SingleGame.objects.get(pk = pk)
        action = request.body

        if action == 'makenewgame':
            game.state = ''
            game.save()
            return HttpResponse()
        else:
            data = game.move_added(action)
            data = {'move':data[0], 'is_won':data[1]}
            print data
            return HttpResponse(json.dumps(data), content_type = "application/json")

        

    

