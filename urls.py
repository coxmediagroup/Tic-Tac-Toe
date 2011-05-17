from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


app_name = settings.APP_NAME

urlpatterns = patterns('',
    # Examples:
    url(r'^$', "{0}.game.views.index".format(app_name), name='home'),
    url(r'^board$', "{0}.game.views.board".format(app_name), name='board'),
    url(r'^again$', "{0}.game.views.play_again".format(app_name), name='again'),
    # url(r'^tic_tac_toe/', include('tic_tac_toe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
