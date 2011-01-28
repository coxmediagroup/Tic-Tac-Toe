from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

# some constants, for use with the tests
kRoot  = "/"
kLogin = "/accounts/login/"
kGames = "/games/"

def _u(url, suffix):
    end = '?' if url.endswith('/') and len(url) > 1 else ''
    return ''.join(('^', url[1:], end, suffix))

urlpatterns = patterns('',

    # django-supplied parts:
    (r'^admin/', include(admin.site.urls)),
    (_u(kLogin, r'$'), 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),

    # mount the app:
    (_u(kRoot, r'$'), 'DJTickyTack.views.index'),
    (_u(kGames, r'$'), 'DJTickyTack.views.games'),

)
