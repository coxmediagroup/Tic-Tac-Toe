
from django.conf.urls import patterns, url
from tictactoe_ui import views

urlpatterns = patterns('',
	url(r'^/?$',        views.index,    name='index'),
	url(r'^newGame/?$', views.new_game, name='new_game'),
	url(r'^game/(?P<game_id>[a-fA-F0-9\-]+)/?$', views.game,  name='game')
	)