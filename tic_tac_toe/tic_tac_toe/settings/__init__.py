"""
Not included in the Github repo is a local development settings file which
contains some private credential information.  Having a settings directory -
rather than a single settings file allows for easy splitting for settings
for different environments.

"""
from .base import *

try:
    from .development import *
except ImportError:
    pass