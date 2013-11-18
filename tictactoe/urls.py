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
)
