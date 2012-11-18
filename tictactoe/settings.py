# Django settings for tictactoe project.

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Ben Spaulding', 'ben@benspaulding.us'),)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'tictactoe.sqlite'),
    }
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
SECRET_KEY = '18cqh=5l8p_fmh#9xc1hvtb)mtu9@)-is0+-+h$ju*rw&o-q#3'
USE_I18N = True
USE_L10N = True
USE_TZ = True

ROOT_URLCONF = 'tictactoe.urls'
WSGI_APPLICATION = 'tictactoe.wsgi.application'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media_root')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static_root')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'tictactoe', 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'tictactoe', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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


###
# Development settings.
###

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Setup Django Debug Toolbar.
try:
    INTERNAL_IPS
except NameError:
    INTERNAL_IPS = []
INTERNAL_IPS = list(INTERNAL_IPS) + ['127.0.0.1']

try:
    __import__('debug_toolbar')
    INSTALLED_APPS = list(INSTALLED_APPS) + ['debug_toolbar']
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES) + \
            ['debug_toolbar.middleware.DebugToolbarMiddleware']
    # Put toolbar middleware before flatpage middleware, if necessary.
    fp_mware = 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
    if MIDDLEWARE_CLASSES.count(fp_mware):
        i = MIDDLEWARE_CLASSES.index(fp_mware)
        MIDDLEWARE_CLASSES.insert(i, MIDDLEWARE_CLASSES.pop())
except ImportError:
    pass

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}
