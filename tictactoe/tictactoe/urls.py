from django.conf.urls import patterns, include, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'$', include('main.urls')),
)
