from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # include admin urls
    url(r'^admin/', include(admin.site.urls)),

    # views for rendering templaets
    url(r'^$', 'ttt.views.home', name='home'),
    url(r'^play', 'ttt.views.play', name='play'),
    url(r'^about', 'ttt.views.about', name='about'),

    # views for game flow
    url(r'^update/(?P<game>\d+)/play/computer', 'ttt.views.computer_play', name='computer_play'),
    url(r'^update/(?P<game>\d+)/play/challenger/(?P<cell>\w+)', 'ttt.views.human_play', name='human_play'),
    url(r'^update/(?P<game>\d+)/challenger/(?P<name>\w+)', 'ttt.views.update_challenger', name='update_challenger'),
)
