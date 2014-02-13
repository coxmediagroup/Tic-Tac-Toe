
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer

import json
from random import choice
import urlparse

from game.models import Game, Board, PLAYER_NONE
from game.player import Computer


class urlencodeSerializer(Serializer):

    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']

    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'text': 'text/plain',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
        }

    def from_urlencode(self, data, options=None):
        """ handles basic formencoded url posts """
        qs = dict(
            (k, v if len(v) > 1 else v[0])
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self, content):
        pass


class BoardResource(ModelResource):
    class Meta:
        object_class = Board
        excludes = ['id', 'resource_uri']


def _move_computer(game):
    comp = game.who_moves()
    if comp != game.user_token and comp != PLAYER_NONE:
        move = Computer.determine_move(game, comp, game.user_token)
        game[move[0]][move[1]] = comp


class GameResource(ModelResource):
    started = fields.DateTimeField(
        attribute='started', readonly=True, use_in='all')
    user_token = fields.IntegerField(
        attribute='user_token', readonly=True, use_in='all')
    status = fields.CharField(
        attribute='status', readonly=True, use_in='all')
    board = fields.ToOneField(
        BoardResource, '_board', use_in='detail', full=True)

    class Meta:
        resource_name = 'game'
        object_class = Game
        queryset = Game.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'patch']
        serializer = urlencodeSerializer()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        # create a new row
        bundle.obj = Game.create_new(is_user_x=choice([True, False]))

        _move_computer(bundle.obj)

        return bundle

    def obj_update(self, bundle, **kwargs):
        if bundle.obj.is_complete():
            return bundle

        data = json.loads(bundle.request.body)
        if len(data.keys()) == 1:
            key = data.keys()[0]

            assert bundle.obj.user_token == data[key]

            assert bundle.obj.who_moves() == bundle.obj.user_token

            if key == 'upper_left':
                bundle.obj[0][0] = data[key]
            elif key == 'upper_center':
                bundle.obj[1][0] = data[key]
            elif key == 'upper_right':
                bundle.obj[2][0] = data[key]
            elif key == 'center_left':
                bundle.obj[0][1] = data[key]
            elif key == 'center':
                bundle.obj[1][1] = data[key]
            elif key == 'center_right':
                bundle.obj[2][1] = data[key]
            elif key == 'lower_left':
                bundle.obj[0][2] = data[key]
            elif key == 'lower_center':
                bundle.obj[1][2] = data[key]
            elif key == 'lower_right':
                bundle.obj[2][2] = data[key]
            else:
                raise Exception('Invalid move')
        else:
            raise Exception('Invalid patch - too many parameters')

        # make computer move
        _move_computer(bundle.obj)

        return bundle
