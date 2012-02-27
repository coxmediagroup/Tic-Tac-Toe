# custom HTTP Responses that Django doesn't provide

from django.http import HttpResponseRedirect

class HttpResponseSeeOtherRedirect(HttpResponseRedirect):
    """Variant of Django's :class:`django.http.HttpResponseRedirect`.  Redirect
    with status code 303, 'See Other'.  This code indicates that the redirected
    content is not a replacement for the requested content, but a different resource.
    """
    status_code = 303