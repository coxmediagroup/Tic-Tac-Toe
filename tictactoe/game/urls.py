from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('tictactoe.game.views',
        url(r'^$', 'createGame', name='createGame'),
        url(r'^doMove/$', 'doMove', name='doMove'),
    )