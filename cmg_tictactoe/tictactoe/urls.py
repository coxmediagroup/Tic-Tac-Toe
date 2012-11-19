from django.conf.urls import patterns, url
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Game
from .views import GameUpdateView, start_game

urlpatterns = patterns('',
    url(r'^$',
        # TODO: Return only in-progress games, once that code is written.
        ListView.as_view(queryset=Game.objects.all()),
        name='tictactoe_game_list'),
    url(r'^complete/$',
        # TODO: Return only in-progress games, once that code is written.
        ListView.as_view(queryset=Game.objects.all()),
        name='tictactoe_game_complete_list'),
    url(r'^play/$',
        start_game,
        name='tictactoe_game_create'),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(model=Game),
        name='tictactoe_game_detail'),
    url(r'^(?P<pk>\d+)/play/$',
        GameUpdateView.as_view(),
        name='tictactoe_game_update'),
)
