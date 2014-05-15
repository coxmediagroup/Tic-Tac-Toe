from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TicTacToe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('^ttt/', include('tic_tac_toe.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
