from django.conf.urls import patterns, include, url
from tictactoe.game.views import GameView

urlpatterns = patterns('',
    (r'^$', GameView.as_view())
)
