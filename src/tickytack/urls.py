from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

from tickytack.views import board
from tickytack.views import user
from tickytack.views import server
from tickytack.views import clear

urlpatterns = patterns('',
    url(r'^$', board, name="board"),
    url(r'^usermove/$', user, name="user_move"),
    url(r'^srvrmove/$', server, name="server_move"),
    url(r'^clear/$', clear, name="clear_board"),
)