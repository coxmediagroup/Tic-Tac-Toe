from django.conf.urls import patterns, include, url
from django.contrib import admin
import tictactoe_api.urls
import tictactoe_api.views
import tictactoe_ui.urls

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tictactoe_api.views.index', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(tictactoe_api.urls)),
    #url(r'^', include(tictactoe_ui.urls))
)
