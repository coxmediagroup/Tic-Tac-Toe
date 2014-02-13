from django.conf.urls import patterns, include, url

from views import all, get

urlpatterns = patterns('tttui.views',
    url(r'^$', all),
    url(r'^(?P<game_id>\d+)/$', get),
)
