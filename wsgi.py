"""
WSGI config for tic_tac_toe project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, platform

if 'vagrant' in platform.node():
    ENV = 'dev'
elif 'prod' in platform.node():
    ENV = 'prod'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tic_tac_toe.settings." + ENV)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
