from django.views.generic import TemplateView
from django.shortcuts import redirect

class HomepageView(TemplateView):
	template_name = "index.html"
