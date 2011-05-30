import os
import sys

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.append(SITE_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()