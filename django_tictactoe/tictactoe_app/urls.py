from django.conf.urls import patterns, include, url
from django.contrib import admin
import tictactoe_api.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe_app.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(tictactoe_api.urls))
)
