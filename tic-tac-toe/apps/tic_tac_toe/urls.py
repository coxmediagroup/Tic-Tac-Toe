from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from tic_tac_toe.views.api import *


# web api
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="tic_tac_toe.html")),
)

# rest api
# urlpatterns += patterns('api/v1/',)