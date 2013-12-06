from django.views.generic import View
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.shortcuts import render
from dict2xml import dict2xml
import json


class CBVBase(View):
    """
    This is the base object for Class Based Views

    The utility methods just make it easier to return a response from the
    the actual view method.
    """
    def to_template(self, template = None, data = {}, ci = None, content_type = None, status = None):
        # process data if necessary
        # automatically select template if one is not specified
        if not ci:
            ci = RequestContext(self.request)
        response = render(self.request, template_name = template, dictionary = data, context_instance = ci, content_type = content_type)
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


