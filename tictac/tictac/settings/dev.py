# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('db', 'dev.sqlite3')},
}

INSTALLED_APPS += ("debug_toolbar", )

MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware", )

