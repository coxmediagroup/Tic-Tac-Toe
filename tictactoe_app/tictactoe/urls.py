
from django.conf.urls import patterns, url
from tictactoe import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^game/$', views.game, name='game'),
	url(r'^game/(?P<game_id>[a-zA-Z0-9\-]+)/$', views.game, name='game')
	)