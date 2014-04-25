from django.conf.urls import patterns, include, url

import tictactoe.views

urlpatterns = patterns('',
    url(r'^$', tictactoe.views.say_hello),
    url(r'^handle-move/$', tictactoe.views.handle_move),
)
