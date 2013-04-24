from django.conf.urls import patterns, include, url

from .api import EventResource

event_resource = EventResource()

urlpatterns = patterns(
    '',
    url(r'^api/', include(event_resource.urls)),
)
