'''API serializers'''

from drf_compound_fields.fields import ListField
from rest_framework.serializers import IntegerField, HyperlinkedModelSerializer

from .models import Game


class GameCreateSerializer(HyperlinkedModelSerializer):
    board = ListField(
        IntegerField(), source='board.board', read_only=True)
    next_moves = ListField(
        IntegerField(), source='board.next_moves', read_only=True)

    class Meta:
        model = Game
        fields = ('url', 'board', 'next_moves', 'server_player', 'winner')
        read_only_fields = ('winner', )


class GameUpdateSerializer(HyperlinkedModelSerializer):
    board = ListField(
        IntegerField(), source='board.board', read_only=True)
    next_moves = ListField(
        IntegerField(), source='board.next_moves', read_only=True)

    class Meta:
        model = Game
        fields = ('url', 'board', 'next_moves', 'server_player', 'winner')
        read_only_fields = ('winner', 'server_player')
