from django.conf.urls import patterns, include, url
from tictactoe.apps.game.views import GameBoardView, SubmitMoveView

urlpatterns = patterns('',
    url(r'^$', GameBoardView.as_view(), name='gameboard'),
    url(r'^submit-move/$', SubmitMoveView.as_view(), name='submit')
)
