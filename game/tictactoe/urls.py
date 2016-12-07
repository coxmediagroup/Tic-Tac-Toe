from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name="base.html")),
    url(r'^play/$', views.play, name='tictactoe.play'),
    url(r'^makemove/$', views.make_move, name='tictactoe.make_move')
)
