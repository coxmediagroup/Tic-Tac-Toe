# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('game.views',
    url(r'^$', 'index', name='index'),
    url(r'^current/$', 'index', name='current'),
)
