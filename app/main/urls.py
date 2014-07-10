from django.conf.urls import patterns, include, url
from django.contrib import admin

from main.views import home_view

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'main.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home_view, name='home_view'),
)
