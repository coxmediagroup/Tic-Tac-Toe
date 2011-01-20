from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()


import DJTickyTack

urlpatterns = patterns('',

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),


    # mount the app:
    (r'^$', 'DJTickyTack.views.index'),
)
