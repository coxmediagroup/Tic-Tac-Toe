from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',

	url(r'^$', views.welcome, name='welcome'),
	url(r'^player/(?P<xplayer>[-A-Za-z0-9_]+)/$', views.game, name='titctactoe_game')

)
