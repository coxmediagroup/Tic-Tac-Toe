from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mm_tictactoe/', include('mm_tictactoe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$', 'mm_tictactoe.tictactoe.views.home'),
    (r'^home/$', 'mm_tictactoe.tictactoe.views.home'),
    (r'^login/', 'mm_tictactoe.tictactoe.views.login'),
    (r'^game/', 'mm_tictactoe.tictactoe.views.game'),
    (r'^newGame/', 'mm_tictactoe.tictactoe.views.newGame'),
)
