from django.conf.urls import patterns, include, url

from tictac.views import (welcome, game_board, )


urlpatterns = patterns('',
    url(r'^$', 'tictac.views.welcome', name='tictac_welcome'),

    url(r'game/board', 'tictac.views.game_board', name='tictac_game_board'),

)
