from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^game/$', 'tic_tac_toe_game.views.game'),
    url(r'^process-player-move/', 'tic_tac_toe_game.views.process_player_move'),
    url(r'^results/$', 'tic_tac_toe_game.views.results'),
)