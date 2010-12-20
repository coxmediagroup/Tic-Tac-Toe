from django.conf.urls.defaults import *
from views import ticTacToe, ticTacToeMove

urlpatterns = patterns('',

    url(r'^ticTacToe/$', ticTacToe, name="ticTacToe"),
    url(r'^move/(?P<board>[_xo]{9})/(?P<player>[xo]{1})/$', ticTacToeMove, name="getMove"),

)
