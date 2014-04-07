from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('', 
	url(r'^js/index.html$','tic.views.index'),
	url(r'^js/(?P<opick>\w)/tic.js$', 'tic.views.createBoard'),  
	url(r'^js/(?P<opick>\w)/(?P<pk>\d+)/tic.js$', 'tic.views.updateBoard',name='update'),
	url(r'^$', 'tic.views.index'),  
)

