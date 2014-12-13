
from django.conf.urls import patterns, url
from tictactoe_api import views

urlpatterns = patterns('',
	url(r'^$', views.list_games, name='index'),
	url(r'^game/(?P<game_id>[a-zA-Z0-9\-]+)/makeMove$', views.make_move, name='make_move'),
	url(r'^game/(?P<game_id>[a-zA-Z0-9\-]+)$', views.get_game, name='get_game'),
	url(r'^game/new$', views.new_game, name='new_game'),
	)