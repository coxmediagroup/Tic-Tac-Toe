from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import HomepageView

urlpatterns = patterns('',

    url(r'^$', HomepageView.as_view(), name='home'),
    url(r'^game/', include('game.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
