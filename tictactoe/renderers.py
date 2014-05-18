from django.core.urlresolvers import reverse
from django.template import RequestContext
from rest_framework.renderers import TemplateHTMLRenderer
import json


class HTMLRenderer(TemplateHTMLRenderer):
    '''
    TemplateHTMLRenderer customized for tictactoe

    Two main changes:
    - The template name is based on the model and action
    - The data is pased in as 'data' in context, not as the context
    '''

    def resolve_context(self, data, request, response):
        '''Pass in the data as context varables'''
        context = {
            'data': data,
            'data_json': json.dumps(data),
        }
        if getattr(request, 'is_captive', False):
            context['next_game_url'] = reverse('start-game')
        else:
            context['next_game_url'] = reverse('game-list') + '?format=html'

        return RequestContext(request, context)

    def get_template_names(self, response, view):
        '''Get a standard template name based on model and action'''
        assert view.model
        model_name = view.model.__name__.lower()
        action = view.action
        return ['tictactoe/{}-{}.jinja2'.format(model_name, action)]
