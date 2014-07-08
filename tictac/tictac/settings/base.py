# -*- coding: utf-8 -*-
"""                                 ,----,                   ,----,
           ,----..                ,'   .`|                 ,'   .`|
          /   /   \ __     ,__  ,`   :'  :               ,`   :'  :
         /   .     :  \   / \_;    ;`   .`             ;    ;`   .`
        .   /   _   \ `\ /  .`__,'    ,'             .`__,'    ,',---.
       .   ;   / `. ;\  /  /|   :     |              |   :     |'   ,'\
   ,---;   |  ; \ ; | \/  / ;   |.';  ;,--.--.   ,---;   |.';  /   /   |,---.
  /    |   :  | ; | '   .' / ---'  |  /  /    \ /    `---'  | .   ; ,. /     \
 /    /.   |  ' ' ' :\  ;  ;   '   : .--.  .-. /    / _ '   : '   | |:/    /  |
.    ' '   ;  \/ / .'    \  \  |   |  \__\/: ..    ' /  |   | '   | ..    ' / |
'   ; :_\   \  ``  /  /\  \  \ '   :  ," .--.;'   ; :__ '   : |   :  '   ;   /.
'   | '.';   :    /  / /\  ;  \'   |./  /  ,. '   | '.' |   |.'\   \ '   |  / |
|   :    :\   \ .'  / /  \  \__\---' ;  :   .' \   :    ;---'   `----|   :    ;
 \   \  /  `---` \ / /    \ /  /     |  ,     .-\   \  /              \   \  /
  `----'          ``'      `--`       `--`---'   `----'                `----'
  .:[  s e t t i n g s  ]:.
"""
from __future__ import unicode_literals

from os.path import join as joinpath, abspath, dirname, basename, realpath


# ID of the current site in the django_site table.
SITE_ID = 1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(g%$zefou7!tmjm2n7!+%%5=pn74@zfu34p7n#_e2aic^c=*p5'
FLASK_SECRET_KEY = '5610b66b69aa4e238b255fa1df340e50' \
                   'fc593a32222d602e65be2c4a4007ee44'
ALLOWED_HOSTS = []

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True


# Paths
###############################################################################
here = lambda *dirs: abspath(joinpath(dirname(__file__), *dirs))
PROJECT_ROOT = here("..", "..")
root = lambda *dirs: abspath(joinpath(PROJECT_ROOT, *dirs))
PROJECT_NAME = basename(PROJECT_ROOT)
APPS_ROOT = root('apps')
SITE_ROOT = root('..', 'site')


# Language and time zone
###############################################################################

# Translation
USE_I18N = False

# Localization
USE_L10N = True

# Time zone aware datetime
USE_TZ = True

# Time zone
TIME_ZONE = 'America/Los_Angeles'

# ISO 639-1 language code
LANGUAGE_CODE = 'en'

# Cachine
###############################################################################

# Use local/development memcached instances
# MEMCACHED_SERVERS = ['127.0.0.1:11211']
# CACHES = {
#     'default': {
#         'BACKEND': 'caching.backends.memcached.MemcachedCache',
#         'LOCATION': MEMCACHED_SERVERS,
#         'PREFIX': 'tictac:',
#     },
#     Set as default if you need to use locmem instead of memcached
#     'locmem': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'default'
#     },
# }
# CACHE_COUNT_TIMEOUT = 60 * 5


# Middleware
###############################################################################

# Timeout when caching middleware or cache_page() decorator is used
CACHE_MIDDLEWARE_SECONDS = 5

# Cache key prefix
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_NAME + '_'

# A tuple of middleware classes to use.
MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
)


# Staticfiles
###############################################################################

# Absolute path to dir where collectstatic will collect files for deployment
STATIC_ROOT = joinpath(SITE_ROOT, 'static')

# URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = '/static/'

# Additional paths staticfiles app will traverse if FileSystemFinder enabled
STATICFILES_DIRS = (
    root('static'),
)

BOWER_COMPONENTS_ROOT = root('static/vendor/bower')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)


# Templates
###############################################################################

# Template file locations
TEMPLATE_DIRS = (
    root('templates'),
)

# Template loader classes
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# RequestContext processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth'
)


# Applications
###############################################################################
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.coxtactoe',
    'south',
)

BOWER_INSTALLED_APPS = (
    'jquery',
)

ROOT_URLCONF = 'tictac.urls'

WSGI_APPLICATION = 'tictac.wsgi.application'
