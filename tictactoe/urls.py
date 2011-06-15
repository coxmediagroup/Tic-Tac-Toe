from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    'tictactoe.views',
        (r'^$', 'show_game'),
        (r'^make_move/', 'make_move'),
)
