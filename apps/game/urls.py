from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import patterns, include, url
from tic_tac_toe.apps.game import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^setup$', views.setup, name='setup'),
    url(r'^clear$', views.clear, name='clear'),
    url(r'^play$', views.play, name='play'),
    url(r'^thanks$', views.thanks, name='thanks'),
)