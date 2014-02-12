from django.conf.urls import url, patterns, include

urlpatterns = patterns('tic_tac_toe.views',
    url(r'^$', 'index', name='index')
)