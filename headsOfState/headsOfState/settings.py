"""
Django settings for headsOfState project.
"""

import os 
FILE_DIR = os.path.dirname(__file__) 

#this is the directory houses the django project and supplementary files
PROJECT_DIR = os.path.abspath(os.path.join(FILE_DIR, "..", "..")) 

#this is the location of headsOfState django project directory
DJANGO_PROJECT_DIR = os.path.abspath(os.path.join(FILE_DIR, "..")) 

#---------------------used for obtaining sensitive information in project.ini
from ConfigParser import RawConfigParser 
config = RawConfigParser() 
config.read(PROJECT_DIR+ "/.project.ini") 
#---------------------used for obtaining sensitive information in project.ini


SECRET_KEY = config.get('data1', 'SECRET_KEY') 

DEBUG = True

TEMPLATE_DEBUG = True

STATIC_URL = '/static/'

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'south',
	'ticTacToe'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'headsOfState.urls'

WSGI_APPLICATION = 'headsOfState.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DJANGO_PROJECT_DIR, 'db.sqlite3'),
    }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
