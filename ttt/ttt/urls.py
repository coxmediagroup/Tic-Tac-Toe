from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ttt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

	url(r'^$', 'ttt.views.home', name='home'),
	url(r'^signin', 'ttt.views.signin', name='signin'),
	url(r'^play', 'ttt.views.play', name='play'),
    url(r'^update/(?P<game>\d)/computer', 'ttt.views.computer_play', name='computer_play'),
    url(r'^update/(?P<game>\d)/challenger/(?P<name>\w)', 'ttt.views.update_challenger', name='play'),
)
