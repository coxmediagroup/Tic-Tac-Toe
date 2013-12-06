from django.conf.urls import patterns, include, url
from .views import TicTacToeView

urlpatterns = patterns('',
    url(r'^$', TicTacToeView.as_view(), name='tictactoe')
)

