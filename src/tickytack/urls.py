from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

from tickytack.views import board
from tickytack.views import move
from tickytack.views import clear

urlpatterns = patterns('',
    url(r'^$', board, name="board"),
    url(r'^init/$', clear, name="init_game"),
    url(r'^move/$', move, name="move"))
