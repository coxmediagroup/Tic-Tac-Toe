from django.views.generic import CreateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import BaseFormView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.utils.decorators import method_decorator

from . import models, forms
import json


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

    def get_context_data(self, **kwargs):
        context = {'position': self.object.positions.latest()}
        context.update(kwargs)
        return super(GameDetailView, self).get_context_data(**context)


class SubmitMoveView(SingleObjectMixin, BaseFormView):
    model = models.Game
    form_class = forms.MoveForm

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            position = self.object.positions.latest()
            return self.render_to_json_response(
                {'error': "You are not authorized to submit"
                 " turns for this game.",
                 'state': position.state,
                 'done': position.is_finished()},
                status=400
            )
        return super(SubmitMoveView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            position = self.object.positions.latest()
            return self.render_to_json_response(
                {'error': "You are not authorized to submit"
                 " turns for this game.",
                 'state': position.state,
                 'done': position.is_finished()},
                status=400
            )
        return super(SubmitMoveView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SubmitMoveView, self).get_form_kwargs()
        kwargs.update(game=self.object)
        return kwargs

    def form_valid(self, form):
        row = form.cleaned_data.get('row')
        column = form.cleaned_data.get('column')
        new_position = self.object.positions.latest().new((row, column))

        if not new_position.is_finished():
            next_move = models.NextMove.objects.lookup(new_position.state)
            new_position = new_position.new(next_move)

        data = {'state': new_position.state,
                'done': new_position.is_finished()}
        return self.render_to_json_response(data)

    def form_invalid(self, form):
        position = self.object.positions.latest()
        data = {'state': position.state,
                'done': position.is_finished()}
        data.update(**form.errors)
        return self.render_to_json_response(data, status=400)
