from django.http                  import HttpResponse, HttpResponseRedirect

from django.views.decorators.http import require_GET, require_POST, \
                                         require_http_methods

from game.models import Game

@require_GET
def all(request):
    """
    List all games
    """
    games = Game.objects.all()
    game_record = [(game.id, game.is_complete(), game.who_won()) for game in games]
    return HttpResponse(str(game_record))

@require_GET
def get(request, game_id):
    """
    Get a game
    """
    game = Game.objects.get(pk=game_id)
    game_record = [(game.id, game.is_complete(), game.who_won())]
    return HttpResponse(str(game_record))

@require_POST
def new(request):
    """
    Create a new game and redirect to it
    """
    pass

@require_POST
def move(request, game_id):
    """
    Post a move to a game
    """
    pass

