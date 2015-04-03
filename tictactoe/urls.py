from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(pattern_name='game:index'), name='index'),
    url(r'^game/', include('game.urls', namespace='game')),
    url(r'^admin/', include(admin.site.urls)),
)
