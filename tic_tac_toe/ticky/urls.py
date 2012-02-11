from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template

import views

urlpatterns = patterns('',
    url(r'^$', views.gameboard, name='gameboard'),
    url(r'^play/$', views.play, name='play'),

    url(r'^about/$', direct_to_template, {'template': 'ticky/about.html'},
        name='about'),
)
