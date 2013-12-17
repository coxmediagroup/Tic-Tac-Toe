from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from . import views


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="tictactoe/main.html"),
        name='main'),
    url(r'^create/$', views.CreateGameView.as_view(), name='create_game'),
)
