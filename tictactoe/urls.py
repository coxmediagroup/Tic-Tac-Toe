from django.conf.urls import patterns, include, url

from django.contrib import admin
from game.views import GameView, PlayerMove

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', GameView.as_view(), name="home"),
    url(r'move$', PlayerMove.as_view(), name="player_move"),
    url(r'^admin/', include(admin.site.urls)),
)
