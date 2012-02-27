import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tictactoe.settings'
os.environ['VIRTUAL_ENV'] = '/home/httpd/Tic-Tac-Toe/env/'

# Note that you shouldn't need to set sys.path here if in the apache config
# you pass the python-path option to WSGIDaemonProcess as described in the
# sample config.

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()