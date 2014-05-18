from django.conf.urls import include, patterns, url

from .views import router

urlpatterns = patterns(
    'tictactoe.views',
    url(r'^$', 'home', name='home'),
    url(r'^about$', 'about', name='about'),
    url(r'^api/', include(router.urls)),
    url(r'^game/$', 'play_game', {'game_id': None}, name='start-game'),
    url(r'^game/(?P<game_id>\d+)/$', 'play_game', name='play-game'),
)
