"""
URLs for game app.
"""
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',                      'game.views.new_game',  name="new_game"),
    url(r'^(?P<game_id>\d+)/$',     'game.views.show_game', name="show_game"),
    url(r'^(?P<game_id>\d+)/move$', 'game.views.make_move', name="make_move"),
)
