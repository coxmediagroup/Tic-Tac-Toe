from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc):
    response = exception_handler(exc)
    if response is None:
        response = Response(
            {'detail': 'Internal Server Error: %s' % (exc,)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    response.data['status_code'] = response.status_code
    response.data['success'] = False
    return response
