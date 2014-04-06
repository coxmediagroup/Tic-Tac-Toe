from annoying.decorators import ajax_request, render_to
from django.views.decorators.csrf import csrf_exempt
from .models import Game


@render_to('client/home.html')
def home(request):
    return {}

@csrf_exempt
@ajax_request
def new_game(request):
    name = request.POST.get('name', None)
    if name:
        game = Game(name=name)
        game.save()
        result = {
            'id' : game.id
        }
    else:
        result = {
            'error' : "'name' field is required."
        }

    return result