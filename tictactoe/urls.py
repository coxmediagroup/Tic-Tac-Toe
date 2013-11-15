from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from tictactoe.api import BoardList, BoardDetail

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # 'Home' Page
    url(r'^$', 'tictactoe.views.game_view', name='home'),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),

    # Django Rest Framework Authentication
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # GameBoard API
    url(r'^api/boards/$', BoardList.as_view()),
    url(r'^api/boards/(?P<pk>[0-9]+)/$', BoardDetail.as_view()),
)
