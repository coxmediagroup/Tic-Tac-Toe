from django.shortcuts import redirect, get_object_or_404, render_to_response
from game.models import Game

def new_game(request):
    "Create a new game and redirect to its url."
    game = Game.objects.create()
    return redirect(game)

def show_game(request, game_id):
    "Show a specific game."
    game = get_object_or_404(Game, pk=game_id)
    return render_to_response("game/show_game.html", { 'game': game })
