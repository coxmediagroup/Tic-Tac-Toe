from django.conf.urls import patterns, include, url
from django.contrib import admin
from tic_tac_toe import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TicTacToe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^move/(?P<row_id>\d+)/(?P<column_id>\d+)/?$', views.make_move, name='index'),

    url(r'^admin/', include(admin.site.urls)),
)
