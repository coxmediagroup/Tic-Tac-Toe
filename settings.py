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
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

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
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'game': {
            'handlers':['console'],
            'level':'DEBUG',
            'propagate': True,
        },
    }
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    #'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

INTERNAL_IPS = ('67.176.120.241','127.0.0.1','192.168.1.2','192.168.1.25')

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    #'SHOW_TOOLBAR_CALLBACK': None,
    #'EXTRA_SIGNALS': ['employees.MySignal', etc.],
    'ENABLE_STACKTRACES': True,
    #'MEDIA_URL': MEDIA_URL + 'debug_toolbar/',
}

#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#        'LOCATION': 'tic-tac-toe',
#    }
#}
