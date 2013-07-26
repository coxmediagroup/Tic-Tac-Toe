from django.conf.urls import patterns, url

from tic import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new-game/', views.new_game, name='new-game'),
    url(r'^player-move/$', views.player_move, name='player-move'),
)

