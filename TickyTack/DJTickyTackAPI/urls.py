from django.conf.urls.defaults import *
from piston.resource import Resource
from DJTickyTackAPI.handlers import GameHandler, JoinHandler

game_handler = Resource(GameHandler)
join_handler = Resource(JoinHandler)

urlpatterns = patterns('',
   url(r'^game/', game_handler), # get game list, post to create move
   url(r'^game/(<?P=id>\d+)', game_handler), # get state, post move
   url(r'^game/joinable/',    join_handler), # get joinables
   url(r'^game/joinable/id', join_handler),  # post to join
)
