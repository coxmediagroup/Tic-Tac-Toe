from django.conf.urls import patterns, url
import tictactoe.views


urlpatterns = patterns(
    '',
    url(r'^$', tictactoe.views.PlayGameView.as_view(), name='play-game'),
    url(r'^mark/$', tictactoe.views.MakeMarkView.as_view(), name='make-mark'),
    url(r'^game-over/$',
        tictactoe.views.GameOverView.as_view(),
        name='game-over',
    ),
)
