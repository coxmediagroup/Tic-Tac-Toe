from django.conf.urls import patterns, include, url

from .views import GameView

urlpatterns = patterns('',

    url(r'^(?P<version>.*)$', GameView.as_view(), name = "game"),

)