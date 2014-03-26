from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tictactoe.views.IndexView', name='home'),
)
