from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',
    url(r'^$', views.start_game, name='start_game')
)