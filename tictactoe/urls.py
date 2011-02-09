from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # Index page.
    url(r'^$', 'django.views.generic.simple.direct_to_template',
        {'template': 'index.html'}, name="index"),

    # Game app URLs.
    (r'^game/', include('game.urls')),
)

# Serve static content through Django if DEBUG = True.
if settings.DEBUG:
    urlpatterns += patterns('',
        (
            r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
