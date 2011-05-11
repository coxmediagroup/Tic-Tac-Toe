from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

from tickytack.views import board


urlpatterns = patterns('',
    url(r'^$', board, name="board")
)