from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^api/', include(event_resource.urls)),
)
