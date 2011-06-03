from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'tictactoe.views.default', name='default'),
    url(r'^move/$', 'tictactoe.views.move', name='move'),
    url(r'^play/$', 'tictactoe.views.play', name='play'),
)