from django.conf.urls import patterns, url

from TicTacToe import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
