from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tic_tac_toe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.game_view),
    url(r'^(?P<player>[XO])-(?P<game_so_far>([A-C][1-3]-)*[A-C][1-3])/$', views.game_view),

)
