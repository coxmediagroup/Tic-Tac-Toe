from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet

from .models import Game
from .serializers import GameCreateSerializer, GameUpdateSerializer


class AboutView(TemplateView):
    '''About page'''
    template_name = 'tictactoe/about.jinja2'


class GameViewSet(ModelViewSet):
    '''API endpoint for creating, viewing, and playing Games'''
    queryset = Game.objects.all()

    @action()
    def move(self, request, pk):
        game = self.get_object()
        board = game.board
        try:
            position = int(request.DATA.get('position'))
            board.move(position)
        except ValueError as e:
            error = {'position': str(e)}
            return Response(error, status=HTTP_400_BAD_REQUEST)
        if board.next_mark() == game.server_player:
            board.move(game.strategy.next_move(board))
        game.board = board
        game.save()
        return redirect('game-detail', pk=pk)

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('list', 'create'):
            return GameCreateSerializer
        else:
            return GameUpdateSerializer


class HomeView(TemplateView):
    '''Root-level home page'''
    template_name = 'tictactoe/home.jinja2'


# For urlpatterns
about = AboutView.as_view()
home = HomeView.as_view()

# API router
router = DefaultRouter()
router.register(r'games', GameViewSet)
