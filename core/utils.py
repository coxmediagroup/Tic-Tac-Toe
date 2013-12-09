from django.views.generic import View
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.shortcuts import render
from dict2xml import dict2xml
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import resolve
import json
import re


class CBVBaseView(View):
    """
    This is the base object for Class Based Views in this project.
    """
    def dispatch(self, request, *args, **kwargs):
        self.current_site = get_current_site(request)
        self.app_name = resolve(request.path).app_name
        view = self.__class__.__name__
        if view[-4:] == 'View':
            view = view[:-4]
        view = re.sub('(.)([A-Z]{1})', r'\1_\2', view).lower()
        self.view = view
        self.view_template = ['%s/%s.html' % (self.app_name, view)]
        return super(CBVBaseView, self).dispatch(request, *args, **kwargs)


    def to_template(self, template = None, data = {}, ci = None, ct = None, status = None):
        if not template:
            template = self.view_template
        if not ci:
            ci = RequestContext(self.request)
        response = render(self.request, template_name = template, dictionary = data, context_instance = ci, content_type = ct)
        if status:
            response.status_code = status
        return response


    def to_json(self, data = {}, status = 200):
        response = Template("{{ json|safe }}")
        context = RequestContext(self.request, {'json' : json.dumps(data)})
        return HttpResponse(response.render(context), content_type="application/json")


    def to_xml(self, data = {}, status = 200):
        temp = Template("<xml>{{ xml_data|safe }}</xml>")
        rc = RequestContext(self.request, {'xml_data' : dict2xml(data)})
        return HttpResponse(temp.render(rc), content_type="application/xhtml+xml")


