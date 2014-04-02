from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
    url(r'^$', 'main', name='main'),
    url(r'^player_move/(?P<game_id>\d+)/(?P<space_id>\d)/', 'player_move', name='player_move'),
)
