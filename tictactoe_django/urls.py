from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
import settings

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    url(r'^', include('tictactoe_django.tictactoe.urls')),
)
