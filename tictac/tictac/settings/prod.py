# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

from .base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': joinpath(SITE_ROOT, 'db', 'prod.sqlite3')},
}

# Use production memcached instances
MEMCACHED_SERVERS = ['127.0.0.1:11211']
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': MEMCACHED_SERVERS,
    },
}