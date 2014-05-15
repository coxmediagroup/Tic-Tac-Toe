from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('tic_tac_toe.urls', namespace="tic_tac_toe")),
)
