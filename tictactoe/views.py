from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy

from . import models, forms


class CreateGameView(CreateView):
    model = models.Game
    form_class = forms.CreateGameForm
    success_url = reverse_lazy('main')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateGameView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateGameView, self).form_valid(form)
