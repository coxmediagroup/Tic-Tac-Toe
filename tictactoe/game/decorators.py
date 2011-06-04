"""
Custom view decorators for game
"""
from django.http import HttpResponseBadRequest

__author__ = "Nick Schwane"

def ajax_required(func, *args, **kwargs):
    """
    Decorator that requires AJAX requests
    """
    def _dec(request, *args, **kwargs):
        if request.is_ajax():
            return func(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest('AJAX Required')
    return _dec