from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('apps.tictactoe',
    url(r'newgame(/setplayer/(?P<xo>\w))?/?$', 'views.newgame'),
)
