# project/app/urls.py

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',

    url(r'^', views.mainPage, name='main'),

)

