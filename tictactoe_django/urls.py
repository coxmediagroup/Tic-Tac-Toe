from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^tictactoe_django/', include('tictactoe_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^$', 'game.views.index', name='index'),
    url(r'^set-challenger/$', 'game.views.set_challenger', name='set_challenger'),
    url(r'^play/$', 'game.views.play', name='play_game'),
)
