from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^/$', home) ,
	url(r'^/begin/$', begin_board) ,
	url(r'^/post_cpu_move/$', post_cpu_move) ,
	url(r'^/post_your_move/$', post_your_move) ,
)