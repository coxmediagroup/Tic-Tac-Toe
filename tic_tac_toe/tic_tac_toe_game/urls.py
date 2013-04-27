from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^game/$', 'tic_tac_toe_game.views.game'),
    url(r'^results/$', 'tic_tac_toe_game.views.results'),
)