from django.conf.urls.defaults import *
import tictactoe
# from myproject.feeds import LatestEntries, LatestEntriesByCategory

urlpatterns = patterns('',
      (r'^$',  'tictactoe.views.start'),
      (r'^play/$',  'tictactoe.views.play'),
    # Uncomment this for admin:
    #  (r'^admin/(.*)', admin.site.root),
)
