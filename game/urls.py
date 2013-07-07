from django.conf.urls import patterns, include, url

from .views import GameView, AlmostWonView

urlpatterns = patterns('',

    url(r'^(?P<version>.*)$', GameView.as_view(), name = "game"),
    url(r'^loser/$', AlmostWonView.as_view(), name = "loser"),

)