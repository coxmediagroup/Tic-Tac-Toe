from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView

from .core import Player
from .models import Game


class GameUpdateView(UpdateView):
    # TODO: Return only in-progress games, once that code is written.
    queryset = Game.objects.all()

    # TODO: Redirect to detail view if game is over.

    def get_success_url(self):
        # Since the user played successfully, have the bot play again.
        player = Player(grid=self.object.grid)
        player.play()
        self.object.save()

        kwargs = {'pk': self.object.pk}
        if self.object.game_over():
            return reverse('tictactoe_game_detail', kwargs=kwargs)
        return reverse('tictactoe_game_update', kwargs=kwargs)


def start_game(request):
    """
    Creates a Game object, has the bot play, and redirects to the update view.
    """
    game = Game.objects.create()
    player = Player(grid=game.grid)
    player.play()
    game.save()
    return redirect(reverse('tictactoe_game_update', kwargs={'pk': game.pk}))
