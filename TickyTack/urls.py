from django.conf.urls.defaults import *
from django.contrib import admin
from settings import *

admin.autodiscover()

def _u(url, suffix=r'$'):
    end = '?' if url.endswith('/') and len(url) > 1 else ''
    return ''.join(('^', url[1:], end, suffix))

urlpatterns = patterns('',

    # django-supplied parts:
    (r'^admin/', include(admin.site.urls)),
    (_u(kLogin), 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),

    (_u(kLogout), 'django.contrib.auth.views.logout'),

    # mount the app:
    (_u(kRoot), 'DJTickyTack.views.index'),
    (_u(kGames, r'/(?P<gameId>\d+)$'), 'DJTickyTack.views.game'),
    (_u(kGames), 'DJTickyTack.views.games'),
    (_u(kJoin, r'/(\d+)$'), 'DJTickyTack.views.join'),
    (_u(kJoin), 'DJTickyTack.views.joinable'),


    # static files:
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':STATIC_ROOT_DIR})
)
