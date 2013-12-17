from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from . import views


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="tictactoe/main.html"),
        name='main'),
)
