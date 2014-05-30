'''Helper functions added to the jinja2 / jingo environment'''
from django.contrib.staticfiles.templatetags.staticfiles import static
import jingo

jingo.register.function(static)
