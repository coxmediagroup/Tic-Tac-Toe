from django.conf.urls import patterns, include, url

from tictac.views import (welcome, )


urlpatterns = patterns('',
    url(r'^$', 'tictac.views.welcome', name='tictac_welcome'),
)
