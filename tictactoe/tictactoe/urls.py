from django.conf.urls import patterns, include, url
from board.api import api
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),
    url(r'^swagger/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
)
