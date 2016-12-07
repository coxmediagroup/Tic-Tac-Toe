# game_web urls.py
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^checkWin$', 'game_web.game_functions.checkWin', name='checkWin'), 
    url(r'^AI_turn$', 'game_web.game_functions.AI_turn', name='AI_turn'),
    url(r'^', 'game_web.views.index', name='Tic-Tac-Toe'),
)