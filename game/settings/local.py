from .base import *  # NOQA


DATABASES['default'].update({'HOST': 'localhost'})
DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

INSTALLED_APPS += (
    'debug_toolbar',
)
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

STATICFILES_DIRS = (
    os.path.abspath(os.path.join(PROJECT_PATH, 'static')),
)
TEMPLATE_DEBUG = DEBUG
TEMPLATE_STRING_IF_INVALID = 'INVALID_VARIABLE'
