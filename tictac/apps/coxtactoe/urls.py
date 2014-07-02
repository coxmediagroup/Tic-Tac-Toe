# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from coxtactoe import views
from coxtactoe import const as C


__docformat__ = 'restructuredtext en'


urlpatterns = patterns('',
   url(r'^game/(?P<%s>[a-z0-9]{32})/?$' %
       (C.URL_KEY_GAME_ID),
       views.TicTacToeGameView.as_view(),
       name=C.VIEW_NAME_GAME),
   url(r'^$', views.TicTacToeSplashView.as_view(),
       name=C.VIEW_NAME_SPLASH),
)


