from django.conf.urls import patterns, url

from tictactoe.views import LoadTicTacToe, PlayTicTacToeAjax

urlpatterns = patterns(
    '',
    url(r'^home/', LoadTicTacToe.as_view(), name='home'),
    url(r'^ajax/play/', PlayTicTacToeAjax.as_view(), name='play'),
    )
