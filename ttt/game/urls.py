from django.conf.urls import patterns, include, url

from tastypie.api import Api
from api.resources import GameResource, BoardResource

v1_api = Api(api_name='v1')
v1_api.register(GameResource())
v1_api.register(BoardResource())

urlpatterns = patterns('',
  (r'^api/', include(v1_api.urls))
)

