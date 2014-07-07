# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'
import logging as log

from .base import *


log.disable(log.CRITICAL)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('db', 'test.sqlite3')},
}

INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=apps.coxtactoe',
    '--with-progressive',
    '--with-doctest',
]
