from django.conf.urls import patterns, url

from tictactoe.api.views import RecommendedPlay

urlpatterns = patterns('',
    url(r'^api/recommended_play/', RecommendedPlay.as_view(),
        name='recommended_play'),
)
