from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tictactoe.views.IndexView', name='home'),
    url(r'^get_move/$', 'tictactoe.views.get_move'),
    url(r'^reset/$', 'tictactoe.views.IndexView'),
)
