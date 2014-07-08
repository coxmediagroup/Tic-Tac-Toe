# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *

__docformat__ = 'restructuredtext en'


DEBUG = True
TEMPLATE_DEBUG = DEBUG


SOUTH_TESTS_MIGRATE = True
DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('db', 'dev.sqlite3')
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'coxtactoe',
        'USER': 'coxtactoe',
        'PASSWORD': 'c0Xtactoe',
        'HOST': '127.0.0.1'
    }
}

INSTALLED_APPS += ("debug_toolbar", )

MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware", )
