from django.conf.urls import patterns, url


urlpatterns = patterns(
    'game.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<pk>\d+)/$', 'game', name='detail')
)
