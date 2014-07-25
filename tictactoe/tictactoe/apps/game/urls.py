from django.conf.urls import patterns, include, url
from tictactoe.apps.game.views import GameBoardView, SubmitMoveView, ResetGameView

urlpatterns = patterns('',
    url(r'^submit-move/$', SubmitMoveView.as_view(), name='submit'),
    url(r'^reset/$', ResetGameView.as_view(), name='reset'),
    url(r'^$', GameBoardView.as_view(), name='gameboard'),
)
