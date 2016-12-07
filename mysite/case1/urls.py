from django.conf.urls import patterns, include, url
from case1 import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^tango_with_django_project/', include('tango_with_django_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.index, name='index'),
	url(r'^page1/$', views.page1, name='page1'),
	#url(r'^page2/$', views.page2, name='page2'),
    #url(r'^case1/', include('case1.urls')), # ADD THIS NEW TUPLE!
)