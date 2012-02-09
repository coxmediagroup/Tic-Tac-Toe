# Django settings for Tic-Tac-Toe project.

import os

# Define a ROOT function that will create normalized paths, using
# the top level of the container virtualenv as root
VENV_ROOT = os.path.normpath("%s/.." % (
        os.path.join(os.path.dirname(__file__))))
ROOT = lambda base: os.path.join(VENV_ROOT, base)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

from global_settings import *

ADMINS = (
    ('Van Gale', 'vangale@agile.st'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ROOT('Tic-Tac-Toe/Tic-Tac-Toe.db'),
    }
}

TEMPLATE_DIRS = (
    ROOT('Tic-Tac-Toe/templates'),
    ROOT('Tic-Tac-Toe'),
)

#STATICFILES_DIRS = (
#    ROOT('Tic-Tac-Toe/game'),
#)

INSTALLED_APPS += ('debug_toolbar',)

MEDIA_ROOT = ROOT('Tic-Tac-Toe/media/')
STATIC_ROOT = ROOT('Tic-Tac-Toe/static/')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
