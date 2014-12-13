from django.conf.urls import patterns, include, url
from django.contrib import admin
import tictactoe.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe_app.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tictactoe/', include(tictactoe.urls))
)
