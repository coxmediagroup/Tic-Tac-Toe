# this is the wsgi file for the backend app. Make sure the WSGIScriptAlias directive points to this file
# so that the HTML front-end can call the backend app through AJAX
import sys

path = 'Users/matt/www/copper/joshua/flask'
if path not in sys.path:
    sys.path.append(path)

from joshua import app as application
