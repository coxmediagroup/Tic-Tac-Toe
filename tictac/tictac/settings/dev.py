# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG


SOUTH_TESTS_MIGRATE = True
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'coxtactoe',
    #     'USER': 'coxtactoe',
    #     'PASSWORD': 'c0Xtactoe',
    #     'HOST': '127.0.0.1'
    # }
    'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': ':memory:',
    #     'TEST_NAME': ':memory:'},
    # 'sqlite3disk': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('db', 'dev.sqlite3')},
}

INSTALLED_APPS += ("debug_toolbar", )

MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware", )


LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'level': 'WARNING', # message level to be written to console
        },
    },
    'loggers': {
        '': {
            # this sets root level logger to log debug and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False, # this tells logger to send logging message
                                # to its parent (will send if set to True)
        },
        'django.db': {
            # django also has database level logging
        },
    },
}


