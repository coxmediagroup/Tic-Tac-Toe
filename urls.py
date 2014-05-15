from django.conf.urls.defaults import include, patterns, url
#from django.contrib import admin

# Uncomment the next two lines to enable the admin:
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'', include('Game.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
