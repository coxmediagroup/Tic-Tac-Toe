from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

from main.views import home_view, BoardView, make_a_move

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^board/?$', BoardView.as_view(), name='home_view'),
    url(r'^ajax/make_a_move/?$', make_a_move, name='make_a_move'),
    url(r'^$', home_view, name='home_view'),
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
