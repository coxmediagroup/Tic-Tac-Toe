from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import t3

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'core.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^t3/', include('t3.urls')),
    url(r'^$', t3.views.index, name='index'),
)
