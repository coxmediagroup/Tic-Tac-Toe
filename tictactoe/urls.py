from django.conf.urls import patterns, include, url
from django.contrib import admin

from tictactoe.api.views import RecommendedPlay
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/recommended_play/', RecommendedPlay.as_view(),
        name='recommended_play'),
)
