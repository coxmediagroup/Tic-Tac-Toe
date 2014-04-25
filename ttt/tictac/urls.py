from django.conf.urls import patterns, include, url

from tictac.views import (welcome, game_board, )


urlpatterns = patterns('',
    url(r'^$', 'tictac.views.welcome', name='tictac_welcome'),

    url(r'game/new', 'tictac.views.new_game', name='tictac_new_game'),
    url(r'game/board', 'tictac.views.game_board', name='tictac_game_board'),
    url(r'game/board/(?P<game_id>\d+)', 'tictac.views.game_board', name='tictac_game_board'),
    url(r'game/play', 'tictac.views.make_play', name='tictac_make_play'),

)
