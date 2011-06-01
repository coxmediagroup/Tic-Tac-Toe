from django.conf.urls.defaults import *
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('views',
    # Example:
    # (r'^tictactoe/', include('tictactoe.foo.urls')),
	
	url(r'^$', 'start_game', name='startGameUrl'),
	url(r'^move/(\d+)$', 'make_move', name='makeMoveUrl'),
	
	
)
