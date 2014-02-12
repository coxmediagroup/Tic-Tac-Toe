from django.conf.urls import patterns, include, url

from views import all, new, get, move

urlpatterns = patterns('game.views',
    # GET methods
    url(r'^$', all),
    url(r'^(?P<game_id>\d+)/$', get),
    # POST methods
    url(r'^new$', new),
    url(r'^(?P<game_id>\d+)/move$', move),
)
