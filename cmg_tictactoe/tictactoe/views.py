from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView

from .models import Game


class GameUpdateView(UpdateView):
    # TODO: Return only in-progress games, once that code is written.
    queryset = Game.objects.all()

    # TODO: Redirect to detail view if game is over.

    def get_success_url(self):
        kwargs = {'pk': self.object.pk}
        if self.object.game_over():
            return reverse('tictactoe_game_detail', kwargs=kwargs)
        return reverse('tictactoe_game_update', kwargs=kwargs)


def start_game(request):
    game = Game.objects.create()
    return redirect(reverse('tictactoe_game_update', kwargs={'pk': game.pk}))
