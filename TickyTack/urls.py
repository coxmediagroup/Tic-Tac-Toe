from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

# some constants, for use with the tests
kRoot  = "/"
kLogin = "/accounts/login/"
kGames = "/games/"
kJoin = "/join/"


def _u(url, suffix=r'$'):
    end = '?' if url.endswith('/') and len(url) > 1 else ''
    return ''.join(('^', url[1:], end, suffix))

urlpatterns = patterns('',

    # django-supplied parts:
    (r'^admin/', include(admin.site.urls)),
    (_u(kLogin), 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),

    # mount the app:
    (_u(kRoot), 'DJTickyTack.views.index'),
    (_u(kGames), 'DJTickyTack.views.games'),
    (_u(kJoin, r'/(\d+)$'), 'DJTickyTack.views.join'),
    (_u(kJoin), 'DJTickyTack.views.joinable'),
)
