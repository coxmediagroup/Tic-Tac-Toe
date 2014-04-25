from django.conf.urls import patterns, include, url

import tictactoe.views

urlpatterns = patterns('',
    url(r'^$', tictactoe.views.say_hello),
)
