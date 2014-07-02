from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.http import HttpResponsePermanentRedirect


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin$', lambda request: HttpResponsePermanentRedirect('admin/')),
    url(r'^api/', include('api.urls')),
    url(r'^/?', include('coxtactoe.urls')),
)
