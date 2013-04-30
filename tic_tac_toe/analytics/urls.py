from django.conf.urls import patterns, include, url
from tastypie.api import Api
from .api import EventResource

v1_api = Api(api_name='v1')
v1_api.register(EventResource())

urlpatterns = patterns(
    '',
    url(r'^api/', include(v1_api.urls)),
)
