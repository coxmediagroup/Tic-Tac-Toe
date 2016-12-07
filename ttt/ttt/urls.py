from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tictac import urls as tictac_urls

urlpatterns = patterns('',
    url(r'^', include(tictac_urls)),
    url(r'^admin/', include(admin.site.urls)),
)
