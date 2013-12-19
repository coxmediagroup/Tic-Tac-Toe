from django.views.generic import CreateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from . import models, forms


class CreateGameView(CreateView):
    model = models.Game
    form_class = forms.CreateGameForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateGameView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(CreateGameView, self).form_valid(form)

        # create the starting position and the AI's first play
        blank = self.object.positions.create()
        next_move = models.NextMove.objects.lookup(blank.state)
        ai_position = blank.new(next_move)

        return response


class GameDetailView(DetailView):
    model = models.Game
    context_object_name = 'game'
