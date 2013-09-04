
from django.conf.urls.defaults import *

from .views import TicTacToeViewController


urlpatterns = patterns('',
    url(r'^$', TicTacToeViewController.as_view()),
    url(r'^move/(?P<move>\d{1})/$', TicTacToeViewController.as_view()),
    url(r'^new/(?P<sign>[X,O]{1})/$', TicTacToeViewController.as_view()),
)
