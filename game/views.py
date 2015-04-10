from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404

from .forms import NewGameForm, PlayForm
from .models import Game


@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        form = NewGameForm(request.POST)
        # Theoretically the only way this form can be invalid
        # is in the case of progammer error or malfeasance --
        # the user doesn't have anything to do.
        if form.is_valid():
            game = form.create()
            # In case the computer is X, it goes first.
            game.play_auto()
            game.save()
            return redirect(game)
    else:
        form = NewGameForm()
    return render(request, 'game/game_list.html', {'form': form})


@require_http_methods(["GET", "POST"])
def game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == "POST":
        # Check for index.
        form = PlayForm(request.POST)
        if form.is_valid():
            game.play(form.cleaned_data['index'])
            game.play_auto()
            game.save()
            # Redirect to the same URL so we don't get resubmission warnings.
            # This is a relatively dumb UI; what you would really
            # want to do is have a front-end UI that does requests via
            # AJAX (jQuery or Ember)
            return redirect(game)
        else:
            # What to do? This is a programmer error for now.
            pass

    return render(request, "game/game_detail.html", {
        'game': game
    })
