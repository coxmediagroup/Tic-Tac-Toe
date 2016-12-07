import socket


hostname = socket.gethostname()

# flake8: noqa
if hostname == 'some_production_host':
    from .production import *
else:
    from .local import *
