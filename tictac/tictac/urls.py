# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.http import HttpResponsePermanentRedirect
from django.contrib import admin

__docformat__ = 'restructuredtext en'

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin$', lambda request: HttpResponsePermanentRedirect('admin/')),
    url(r'^/?', include('apps.coxtactoe.urls')),
)
