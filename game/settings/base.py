"""
Django settings for game project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os


PROJECT_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                             os.path.pardir, os.path.pardir))
PROJECT_NAME = 'tictactoe'

ADMINS = (
    ('Percy Perez', 'percyp3@gmail.com'),
)
ALLOWED_HOSTS = []
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/tictactoe.db',
        'USER': PROJECT_NAME,
        'PASSWORD': PROJECT_NAME,
        'HOST': '',
    }
}
DEBUG = False

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # LIBRARIES
    # LOCAL APPS
    'game.tictactoe'
)
INTERNAL_IPS = ('127.0.0.1',)
LANGUAGE_CODE = 'en-us'
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'game.urls'
SECRET_KEY = 'ltvg@0@qg=1elq^@m_r)!z0-bi#qmer@jr1$q+mj5q@&$t-u6&'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)
TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, 'game', 'templates'),)
TIME_ZONE = 'UTC'

USE_I18N = False
USE_TZ = True

WSGI_APPLICATION = 'game.wsgi.application'
