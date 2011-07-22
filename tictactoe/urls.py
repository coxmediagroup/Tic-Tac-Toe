from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import os
from django.views.generic import TemplateView, ListView

admin.autodiscover()

#mysitemaps = {
#    'page' : GenericSitemap({
#        'queryset': Page.objects.all(),
#        'changefreq' : 'monthly',
#        'date_field': 'modification_date',
#    }, priority=0.6),
#}
## OR
# mysitemaps = {'pages' : PageSitemap}

urlpatterns = patterns('',
        (r'^/?$', TemplateView.as_view(template_name="root.html")),
)

# serve static content in debug mode
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
            'show_indexes' : True
        }),
        (r'^(media/|static/)?medialibrary/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': '%s/medialibrary/' % settings.MEDIA_ROOT,
            'show_indexes' : True
        }),
        (r'^(?P<path>favicon.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    )


urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),    
    #(r'sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': mysitemaps}),
)
