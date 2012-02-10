# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('game.views',
    url(r'^new/X/$', 'new_X', name='newX'),
    url(r'^new/O/$', 'new_O', name='newO'),
    url(r'^$', 'index', name='index'),
)
