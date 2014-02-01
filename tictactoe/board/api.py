from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from django.http import Http404
from board.models import Player, Move, Game

class PlayerResource(ModelResource):
  class Meta:
    queryset = Player.objects.all()
    resource_name = 'player'
    authorization = Authorization()
    


api = Api(api_name='v1')
api.register(PlayerResource())
