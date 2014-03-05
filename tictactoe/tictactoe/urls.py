from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('gameinterface.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^gameinterface/', include('gameinterface.urls')),
    url(r'^gameengine/', include('gameengine.urls')),
)
