from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'user_management.views.log'),
    url(r'^usermanagement/', include('user_management.urls')),
    #url(r'^userdirectory/', include('user_directory.urls')),
    #url(r'^analytics/', include('analytics.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
