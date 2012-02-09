from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template, redirect_to

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^convert/', include('lazysignup.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/', include('game.urls', namespace='game')),
    url(r'^$',
        redirect_to,
        { 'url': '/game/', 'permanent': True },
        name='home'),
    #url(r'^$', direct_to_template, {'template': 'index.html'}, "home"),
)

urlpatterns += staticfiles_urlpatterns()
