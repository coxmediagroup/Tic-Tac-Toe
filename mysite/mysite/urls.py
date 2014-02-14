from django.conf.urls import patterns, include, url
#from case1 import views
from django.contrib import admin
admin.autodiscover()




urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$','mysite.views.home', name='home'),
	#url(r'^case1/', include('case1.urls')),
	url(r'^case1/', include('case1.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
