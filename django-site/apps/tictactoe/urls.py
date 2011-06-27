from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('apps.tictactoe',
    url(r'newgame(/size/(?P<size>\d+))?/?$', 'views.newgame'),
    url(r'makemove/x/(?P<x>\d+)/y/(?P<y>\d+)/?$', 'views.makemove'),
    url(r'getmove/?$', 'views.getmove'),
)
