"""
Use for testing on sqlite3...

$ ./manage.py test --settings=game.settings.test game.tictactoe.tests
"""
# flake8: noqa
from base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/test.db',
        'USER': PROJECT_NAME,
        'PASSWORD': PROJECT_NAME,
        'HOST': '',
    }
}
DEBUG = True

INSTALLED_APPS += ('django_nose',)
NOSE_ARGS = [
    '--logging-clear-handlers',
    '--with-progressive',
    '-s',
]

TEMPLATE_DEBUG = DEBUG
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
