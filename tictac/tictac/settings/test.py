# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *

import logging as log
log.disable(log.CRITICAL)

__docformat__ = 'restructuredtext en'


DEBUG = False
TEMPLATE_DEBUG = DEBUG
SOUTH_TESTS_MIGRATE = False

BASE_URL = 'http://127.0.0.1:8000'
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('db', 'test.sqlite3')},
}

INSTALLED_APPS += (
    'django_nose',
    'django_coverage',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=apps.coxtactoe',
    '--with-progressive'
]

# chromedriver must be on path
#SELENIUM_WEBDRIVER = 'chrome'
SELENIUM_WEBDRIVER = 'firefox'

