from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^tictactoe/', include('tictactoe.foo.urls')),

    # Main/Game page 
    (r'^$', 'core.views.play_game'),    
    (r'^make_move/$', 'core.views.make_move'),    

    # Login / logout.
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'core.views.logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
