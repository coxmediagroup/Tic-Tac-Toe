from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^tictactoe/', include('tictactoe.foo.urls')),
    url(r'^tictactoegame/$', 'tictactoegame.views.index'),
    url(r'^tictactoegame/(?P<game_id>\d+)/$', 'tictactoegame.views.detail'),
    url(r'^tictactoegame/play/$', 'tictactoegame.views.play'),
    url(r'^tictactoegame/play/(?P<move_string>\d+)/$', 'tictactoegame.views.play'),
    url(r'^tictactoegame/login/$', 'tictactoegame.views.login'),
    url(r'^tictactoegame/newgame/$', 'tictactoegame.views.newgame'),
    url(r'^tictactoegame/logout/$', 'tictactoegame.views.logout'),
    # url(r'^tictactoegame/(?P<game_id>\d+)/results/$', 'tictactoegame.views.results'),
    # url(r'^tictactoegame/(?P<game_id>\d+)/vote/$', 'tictactoegame.views.vote'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
