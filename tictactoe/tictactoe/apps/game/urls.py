from django.conf.urls import url, patterns


urlpatterns = patterns(
    'game.views',
    url(r'^$', 'index', name='index'),
    url(r'^next-move/$', 'next_move', name='next_move'),
    url(r'^reset/$', 'reset', name='reset'),
)
