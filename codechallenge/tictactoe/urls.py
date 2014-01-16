from django.conf.urls import patterns, url
from . import views

# Tic-Tac-Toe app urls
urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)

