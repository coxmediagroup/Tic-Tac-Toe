import os, sys

app_name = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)).split("/")[-1]

sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, os.pardir)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)))

from django.core.handlers.wsgi import WSGIHandler
os.environ["DJANGO_SETTINGS_MODULE"] = "{0}.settings".format(app_name)
application = WSGIHandler()