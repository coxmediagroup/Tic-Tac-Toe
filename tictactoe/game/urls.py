from django.conf.urls.defaults import *

urlpatterns = patterns('tictactoe.game.views',
    url(r'^$', 'main_view', name="game-main"),
    url(r'^move/$', 'computer_move', name="game-computer-move"),
    url(r'^check/$', 'human_move', name="game-human-move"),
)
