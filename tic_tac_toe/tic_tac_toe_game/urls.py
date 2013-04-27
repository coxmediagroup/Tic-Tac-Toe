from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^play/$', 'tic_tac_toe_game.views.game'),
    url(r'^results/$', 'tic_tac_toe_game.views.game_results'),
)