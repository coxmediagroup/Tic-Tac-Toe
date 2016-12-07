from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'tictactoe.views.home', name='home'),
    url(r'^playeraction$', 'tictactoe.views.playeraction', name='playeraction'),
)
