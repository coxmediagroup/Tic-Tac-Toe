from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # We're going to serve the game from a catch-all URL.
    # Since it's a one-page site, we'll direct all quries that don't
    # match another pattern to the `play` application's `index` view.
    url(r'^$', 'play.views.index', name="index"),
    url(r'^move$', 'play.views.move', name="move"),
    url(r'^new_game$', 'play.views.new_game', name="new_game"),
    url(r'^get_details$', 'play.views.get_details', name="get_details"),
)
