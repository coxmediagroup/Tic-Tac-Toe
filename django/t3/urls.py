from django.conf.urls import patterns, include, url
from t3 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
