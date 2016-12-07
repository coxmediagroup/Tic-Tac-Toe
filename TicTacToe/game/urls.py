from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',
    url(r'^$', views.start_game, name='start_game'),
    url(r'^launch/$', views.launch, name='launch'),
    url(r'^ajax_make_move/(?P<box_choice>\w+)/$', views.ajax_make_move, name='ajax_make_move'),
    url(r'^game/$', views.game_page, name='game'),
)