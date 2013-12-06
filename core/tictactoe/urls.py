from django.conf.urls import patterns, include, url
from .views import TicTacToeView, MoveView

urlpatterns = patterns('',
	url(r'^$', TicTacToeView.as_view(), name='tictactoe'),
	url(r'^$', MoveView.as_view(), name='move')
)

