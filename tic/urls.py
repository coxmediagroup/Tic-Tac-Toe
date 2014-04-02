from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('', 
	url(r'^$', 'tic.views.play'),  

)

