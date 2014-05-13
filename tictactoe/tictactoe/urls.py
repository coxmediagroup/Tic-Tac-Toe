from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tictactoe.controllers.game.new', name='new'),
    url(r'^game', 'tictactoe.controllers.game.index', name='index'),
    url(r'^api/newGame', 'tictactoe.controllers.game.newgame'),
    url(r'^api/play/(\d{1})', 'tictactoe.controllers.game.play'),
    url(r'^api/board', 'tictactoe.controllers.game.returnBoard'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
