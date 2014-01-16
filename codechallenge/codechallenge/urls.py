from django.conf.urls import patterns, include, url
from django.contrib import admin

# locate admin urls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'codechallenge.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('tictactoe.urls')),
    
)

