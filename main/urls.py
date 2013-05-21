from django.conf.urls import patterns, url
import tictactoe.views

urlpatterns = patterns(
    '',
    url(r'^$', tictactoe.views.Game.as_view(), name='game'),
    url(r'^mark/$', tictactoe.views.MakeMark.as_view(), name='make-mark'),
)
