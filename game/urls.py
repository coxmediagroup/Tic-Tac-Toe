from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'game.views.play',name='play'),
)