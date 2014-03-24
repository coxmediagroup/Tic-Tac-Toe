from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^tic-tac-toe/$', views.TicTacToeList.as_view(), name='tictactoe-list'), 
    url(r'^tic-tac-toe/(?P<pk>\d)/$', views.TicTacToeDetail.as_view(), name='tictactoe-detail'), 
    
    # Async urls
    url(r'^tic-tac-toe/next/$', views.TicTacToeNextMove.as_view(), name='tictactoe-ajax'), 
)
