from django.conf.urls import patterns, url


urlpatterns = patterns(
    'tictactoe.views',
    url(r'^$', 'home', name='home'),
    url(r'^about$', 'about', name='about'),
)
