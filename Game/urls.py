from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Game.views import begin_game, game_move, reset_game

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    #root index
    url(
        regex=r'^$',
        view=begin_game,
        name='begin_game'
    ),
    #users_move
    url(
        regex=r'^your_move$',
        view=game_move,
        name='game_move'
    ),
    #reset the game
    url(
        regex=r'^reset$',
        view=reset_game,
        name='reset_game')

)
urlpatterns += staticfiles_urlpatterns()
