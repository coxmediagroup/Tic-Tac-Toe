from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',

	url(r'^$',
		views.welcome,
		name='welcome'),
	url(r'^player/(?P<xplayer>[-A-Za-z0-9_]+)/$',
		views.game,
		name='titctactoe_game'),
	url(r'^player/(?P<players>[-A-Za-z0-9_]+)/(?P<board>[-A-Za-z]+)/$',
		views.ajax_game_result,
		name="game_ajax_game_result"),
	url(r'^result/$',
		views.ajax_game_result,
		name="game_ajax_game_result"),
)
