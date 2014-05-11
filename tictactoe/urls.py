from django.conf.urls import include, patterns, url

from .views import router

urlpatterns = patterns(
    'tictactoe.views',
    url(r'^$', 'home', name='home'),
    url(r'^about$', 'about', name='about'),
    url(r'^api/', include(router.urls)),
)
