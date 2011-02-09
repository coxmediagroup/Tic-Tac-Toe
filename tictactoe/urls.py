from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$',                          'game.views.new_game',  name="new_game"),
    url(r'game/(?P<game_id>\d+)/$',     'game.views.show_game', name="show_game"),
    url(r'game/(?P<game_id>\d+)/move$', 'game.views.make_move', name="make_move"),
)

# Serve static content through Django if DEBUG = True.
if settings.DEBUG:
    urlpatterns += patterns('',
        (
            r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
