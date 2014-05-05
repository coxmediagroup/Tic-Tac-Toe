"""
Use for testing on sqlite3...

$ ./manage.py test --settings=game.settings.test game.tictactoe.tests
"""
import os

# flake8: noqa
from .base import *

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
LIVE_SERVER_PORT = 8081
NOSE_ARGS = [
    '--logging-clear-handlers',
    '--with-progressive',
    '-s',
]
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(PROJECT_PATH, 'static')),
)
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = ('localhost:%i' %
                                                 LIVE_SERVER_PORT)

# Use our own debug context processor for testing, since DEBUG=False for
# LiveServerTests
TEMPLATE_CONTEXT_PROCESSORS += ('game.context_processors.debug',)
TEMPLATE_DEBUG = DEBUG
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
