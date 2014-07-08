# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *

import logging as log
log.disable(log.CRITICAL)

__docformat__ = 'restructuredtext en'


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SOUTH_TESTS_MIGRATE = False

BASE_URL = 'http://127.0.0.1:8000'
ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '192.168.0.100', 'bzdzb.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': root('db', 'test.sqlite3')},
}

INSTALLED_APPS += (
    'django_nose',
    'django_coverage',
)

# TEST_RUNNER = 'testrunner.NoseCoverageTestRunner'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=apps.coxtactoe',
    '--with-progressive',
    '--with-doctest',
]

COVERAGE_MODULE_EXCLUDES = [
    'tests$',
    'settings$',
    'urls$',
    'locale$',
    'migrations',
    'fixtures',
    'admin$',
    'django_extensions',
]
#COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'coverage')

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'stream_to_console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler'
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': here('coxtactoe_debug.log'),
#             },
#         },
#     'loggers': {
#         'django.request': {
#             'handlers': ['stream_to_console'],
#             'level': 'DEBUG',
#             'propagate': True,
#             },
#         'another_random_logger': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#             },
#         }
# }