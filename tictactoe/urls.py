from django.conf.urls import patterns, include, url

from client.views import new_game

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # API
    url(r'^api/new-game/$', new_game, name='new-game'),

    url(r'^admin/', include(admin.site.urls)),
)
