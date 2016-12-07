from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TicTacToe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'tic_app.views.index', name='index'),
    url(r'^send_state_ajax$', 'tic_app.views.process_state_ajax'),
    url(r'^first_move_json$', 'tic_app.views.first_move_ajax'),
    
)
