from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TicTacToe.views.home', name='home'),
    # url(r'^TicTacToe/', include('TicTacToe.foo.urls')),
    url(r'standard/$', 'core.views.standard', name='standard'),
    url(r'standard/move/(?P<move>[0-8])/$', 'core.views.standard', name='move'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
