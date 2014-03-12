from django.conf.urls import patterns, url
from tic_tac_toe import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^move/(?P<row_id>\d+)/(?P<column_id>\d+)/?$', views.make_move, name='index'),
)
