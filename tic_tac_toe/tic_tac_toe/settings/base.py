# Django settings for doulaexchange_env project.
import os
import dj_database_url
from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(3)

DEBUG = False

ADMINS = (
    ('Michael Dunn', 'mike@doulaexchange.com'),
)

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'app9377449@heroku.com'
EMAIL_HOST_PASSWORD = 'ob1wankenob1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.doulaexchange.com','www.doulaexchange.com']

DATABASES = {
    'default': {} # Must create this so that it can be overridden below.
}

DATABASES['default'] = dj_database_url.config()

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Indianapolis'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

MEDIA_ROOT = PROJECT_DIR.child("media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

#STATIC_ROOT = ''
STATIC_ROOT = PROJECT_DIR.child("collectstaticfiles")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    PROJECT_DIR.child("static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rp-k#rafh5%2q^z^jq(ec+pv&amp;9fk$yh1p6&amp;5%l$$ay-htht!n5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "payments.context_processors.payments_settings",)

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'doulaexchange_env.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'doulaexchange_env.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_DIR.child("templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'south',
    'tastypie',
    'payments',
    'django_forms_bootstrap',
    'doulaexchange_env',
    'user_management',
    'user_directory',
    'about_us',
    'homepage',
    'analytics',
    'communications',
    
)

# Extended User Model
AUTH_PROFILE_MODULE = 'user_management.Person'

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


#django-stripe-payments configuration
PAYMENTS_PLANS = {
    "monthly": {
        "stripe_plan_id": "pro-monthly",
        "name": "Web App Pro ($25/month)",
        "description": "The monthly subscription plan to WebApp",
        "price": 25,
        "currency": "usd",
        "interval": "month"
    },
    "yearly": {
        "stripe_plan_id": "pro-yearly",
        "name": "Web App Pro ($199/year)",
        "description": "The annual subscription plan to WebApp",
        "price": 199,
        "currency": "usd",
        "interval": "year"
    }
}

STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", 
                                   "pk_test_EC86Fy5voER8wNGdlKXSAkqD")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", 
                                   "sk_test_CaYqpQbp2zJjAkHCKlvyUuBc")
