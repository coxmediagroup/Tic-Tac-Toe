from django.conf.urls import patterns, url

from tic_tac_toe import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
