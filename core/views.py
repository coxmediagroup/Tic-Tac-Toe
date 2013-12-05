from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render, render_to_response

class HomeView(View):
	def get(self, request):
		context = {}
		return render_to_response("home.html", context, RequestContext(request))


