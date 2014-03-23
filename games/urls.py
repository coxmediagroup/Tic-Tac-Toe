from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^tic-tac-toe/$', views.TicTacToe.as_view(), name='tic_tac_toe'), 
    url(r'^tic-tac-toe/(?P<id>\d)/$', views.TicTacToeStart.as_view(), name='game_page'), 
)
