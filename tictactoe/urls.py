from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static

from tictactoe.api.views import RecommendedPlay

urlpatterns = patterns('',
    url(r'^$', "tictactoe.board.views.index", name="board_index"),
    url(r'^api/recommended_play/', RecommendedPlay.as_view(),
        name='recommended_play'),
)

urlpatterns += static(settings.STATIC_URL,
    document_root=settings.STATIC_ROOT)
