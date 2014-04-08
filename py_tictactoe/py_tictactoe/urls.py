from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'py_tictactoe.views.home', name='home'),
    url(r'^reset$', 'py_tictactoe.views.reset', name='reset'),
    url(r'^play$', 'py_tictactoe.views.play', name='play'),

    # url(r'^admin/', include(admin.site.urls)),
)
