from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ttt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'web.views.get_params', name='get_params'),
    url(r'^start$', 'web.views.start', name='start'),
    url(r'^play/$', 'web.views.play', name='play'),
)
