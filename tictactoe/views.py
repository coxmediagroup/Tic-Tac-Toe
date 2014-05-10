from django.views.generic import TemplateView


class HomeView(TemplateView):
    '''Root-level home page'''
    template_name = 'tictactoe/home.jinja2'


class AboutView(TemplateView):
    '''About page'''
    template_name = 'tictactoe/about.jinja2'


# For urlpatterns
home = HomeView.as_view()
about = AboutView.as_view()
