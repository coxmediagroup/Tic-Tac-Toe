from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from .models import Game
from .serializers import GameSerializer


class AboutView(TemplateView):
    '''About page'''
    template_name = 'tictactoe/about.jinja2'


class GameViewSet(
        CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    '''
    API endpoint for creating, viewing, and playing Games

    To make a move, POST position=(next move) to the move url
    '''
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action()
    def move(self, request, pk):
        game = self.get_object()
        board = game.board
        if 'position' not in request.DATA:
            error = {'position': 'must be a valid next move'}
            return Response(error, status=HTTP_400_BAD_REQUEST)
        try:
            position = int(request.DATA['position'])
            board.move(position)
        except ValueError as e:
            error = {'position': str(e)}
            return Response(error, status=HTTP_400_BAD_REQUEST)
        if board.next_mark() == game.server_player:
            board.move(game.strategy.next_move(board))
        game.board = board
        game.save()
        return redirect('game-detail', pk=pk)


class HomeView(TemplateView):
    '''Root-level home page'''
    template_name = 'tictactoe/home.jinja2'


# For urlpatterns
about = AboutView.as_view()
home = HomeView.as_view()

# API router
router = DefaultRouter()
router.register(r'games', GameViewSet)
