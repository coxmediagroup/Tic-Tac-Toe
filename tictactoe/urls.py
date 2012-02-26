from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^game/', include('tictactoe.game.urls', namespace='game')),
    url(r'^$', 'tictactoe.game.views.index', name="site-index"),
    )

urlpatterns += staticfiles_urlpatterns()