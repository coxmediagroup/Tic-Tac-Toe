from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^tic/', include('tic.urls')),
    url(r'^$', include('tic.urls')),

)
