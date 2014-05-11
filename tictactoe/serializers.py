'''API serializers'''

from drf_compound_fields.fields import ListField
from rest_framework.serializers import IntegerField, HyperlinkedModelSerializer

from .models import Game


class GameCreateSerializer(HyperlinkedModelSerializer):
    board = ListField(
        IntegerField(), source='board.board', read_only=True)
    next_moves = ListField(
        IntegerField(), source='board.next_moves', read_only=True)

    def save_object(self, obj, *args, **kwargs):
        '''If it is the server's turn, take it'''
        board = obj.board
        if board.next_mark() == obj.server_player:
            board.move(obj.strategy.next_move(board))
            obj.board = board
        super(GameCreateSerializer, self).save_object(obj, *args, **kwargs)

    class Meta:
        model = Game
        fields = ('url', 'board', 'next_moves', 'server_player', 'winner')
        read_only_fields = ('winner', )


class GameUpdateSerializer(GameCreateSerializer):
    class Meta(GameCreateSerializer.Meta):
        read_only_fields = ('winner', 'server_player')
