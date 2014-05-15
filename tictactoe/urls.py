from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tictactoe.game.views.index'),
    url(r'^new/$', 'tictactoe.game.views.new_game'),
    url(r'^play/$', 'tictactoe.game.views.render_board'),
    url(r'^move/$', 'tictactoe.game.views.set_move'),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.CWD})
    # url(r'^tictactoe/', include('tictactoe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
