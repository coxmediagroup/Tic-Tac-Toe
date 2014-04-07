from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('', 
	url(r'^tic.js$', 'tic.views.createBoard'),  
	url(r'^(?P<opick>\w)/(?P<pk>\d+)/tic.js$', 'tic.views.updateBoard',name='update'),
	url(r'^$','tic.views.index'),
)

