from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TicTacToe.views.home', name='home'),
    # url(r'^TicTacToe/', include('TicTacToe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ticTacToe.views.index'),
    url(r'^newgame$', 'ticTacToe.views.newGame'),
    url(r'^game/(?P<gameId>\d+)/*$', 'ticTacToe.views.game'),
    url(r'^move/(?P<gameId>\d+)/(?P<xPosition>\d+)/(?P<yPosition>\d+)/(?P<playerMark>\D+)/*$',
		'ticTacToe.views.move'
	)
)
