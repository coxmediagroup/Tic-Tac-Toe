from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^board$', 'tictac.mainapp.views.paint_board'),  
    url(r'^your_move$', 'tictac.mainapp.views.process_move'),    
       
)
