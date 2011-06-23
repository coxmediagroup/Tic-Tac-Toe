from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('apps.tictactoe',
    url(r'newgame(/setplayer/(?P<xo>\w))?/?$', 'views.newgame'),
    url(r'makemove/x/(?P<x>\d+)/y/(?P<y>\d+)/?$', 'views.makemove'),
)
