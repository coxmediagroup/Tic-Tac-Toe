from django.conf.urls import patterns, include, url

from client.views import home, make_move, new_game

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Home
    url(r'^$', home, name='home'),

    # API
    url(r'^api/make-move/$', make_move, name='make-move'),
    url(r'^api/new-game/$', new_game, name='new-game'),

    url(r'^admin/', include(admin.site.urls)),
)
