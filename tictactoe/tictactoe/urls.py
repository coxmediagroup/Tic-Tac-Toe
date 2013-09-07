from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Main/Game page 
    (r'^$', 'core.views.play_game'),    
    (r'^make_move/$', 'core.views.make_move'),    

    # Login / logout.
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'core.views.logout_user'),

    url(r'^admin/', include(admin.site.urls)),
)
