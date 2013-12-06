from django.conf.urls import patterns, include, url
from .views import HomeView

urlpatterns = patterns('',
	url(r'^$', include(patterns('',url(r'^$', HomeView.as_view())), app_name='core')),
    url(r'^tictactoe/', include('core.tictactoe.urls', app_name='tictactoe'))
)

