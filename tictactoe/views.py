from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from .models import Game
from .serializers import GameCreateSerializer, GameUpdateSerializer


class AboutView(TemplateView):
    '''About page'''
    template_name = 'tictactoe/about.jinja2'


class GameViewSet(ModelViewSet):
    '''API endpoint for creating, viewing, and playing Games'''
    queryset = Game.objects.all()

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
