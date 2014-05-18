'''API serializers'''

from drf_compound_fields.fields import ListField
from rest_framework.serializers import (
    HyperlinkedModelSerializer, IntegerField, SerializerMethodField)
from rest_framework.reverse import reverse

from .models import Game


class GameSerializer(HyperlinkedModelSerializer):
    '''
    Serializer for creating, viewing, and updating Game objects
    '''

    board = ListField(
        IntegerField(), source='board.board', read_only=True)
    next_moves = ListField(
        IntegerField(), source='board.next_moves', read_only=True)
    move_url = SerializerMethodField('get_move_url')
    winning_positions = ListField(
        IntegerField(), source='board.winning_positions', read_only=True)

    def get_move_url(self, obj):
        request = self.context.get('request')
        return reverse('game-move', kwargs={'pk': obj.pk}, request=request)

    def save_object(self, obj, *args, **kwargs):
        '''If it is the server's turn, take it'''
        board = obj.board
        if board.next_mark() == obj.server_player:
            board.move(obj.strategy.next_move(board))
            obj.board = board
        super(GameSerializer, self).save_object(obj, *args, **kwargs)

    class Meta:
        model = Game
        fields = (
            'url', 'board', 'next_moves', 'move_url', 'server_player',
            'winner', 'winning_positions')
        read_only_fields = ('winner', )
