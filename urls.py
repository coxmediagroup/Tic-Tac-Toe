from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tic_tac_toe.game.views.index', name='home'),
    url(r'^board$', 'tic_tac_toe.game.views.board', name='board'),
    url(r'^again$', 'tic_tac_toe.game.views.play_again', name='again'),
    # url(r'^tic_tac_toe/', include('tic_tac_toe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
