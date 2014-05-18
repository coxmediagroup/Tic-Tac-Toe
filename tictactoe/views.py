from django.http import HttpResponseRedirect
from django.core.urlresolvers import resolve, reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
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


class GameView(View):
    '''User's interface to games'''

    def dispatch(self, request, game_id, *args, **kwargs):
        if game_id:
            api_url = reverse('game-detail', kwargs={'pk': game_id})
        else:
            api_url = reverse('game-list')
        api_view, api_args, api_kwargs = resolve(api_url)
        request.is_captive = True
        api_kwargs['request'] = request
        api_kwargs['format'] = 'html'
        response = api_view(*api_args, **api_kwargs)
        return response


class CaptiveCreateModelMixin(CreateModelMixin):
    """
    Create a model instance, but act differently if serving the user interface
    """
    @property
    def is_captive(self):
        '''Return True if we are serving the user interface'''
        return getattr(self.request, 'is_captive', False)

    def create(self, request, *args, **kwargs):
        '''
        If captive, redirect to the user interface

        If not captive, default behaviour is to return 201 CREATED on
        success
        '''
        if self.is_captive:
            serializer = self.get_serializer(
                data=request.DATA, files=request.FILES)
            if serializer.is_valid():
                self.pre_save(serializer.object)
                self.object = serializer.save(force_insert=True)
                self.post_save(self.object, created=True)
                headers = self.get_success_headers(serializer.data)
                return HttpResponseRedirect(headers['Location'])
        return super(
            CaptiveCreateModelMixin, self).create(request, *args, **kwargs)

    def get_success_headers(self, data):
        '''If captive, change the Location header to the user interface

        If not captive, default behaviour is to return API URL
        '''
        if self.is_captive and 'id' in data:
            url = reverse('play-game', kwargs={'game_id': data['id']})
            return {'Location': url}
        else:
            return super(
                CaptiveCreateModelMixin, self).get_success_headers(data)


class GameViewSet(
        CaptiveCreateModelMixin, ListModelMixin, RetrieveModelMixin,
        GenericViewSet):
    '''
    API endpoint for creating, viewing, and playing Games

    To make a move, POST position=(next move) to the move url
    '''
    model = Game
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
play_game = GameView.as_view()

# API router
router = DefaultRouter()
router.register(r'games', GameViewSet)
