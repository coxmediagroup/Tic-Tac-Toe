from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',
    url(r'^$', views.game, name='titctactoe_game')
)