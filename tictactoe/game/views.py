from django.shortcuts import render_to_response, redirect
from django.template import Context, RequestContext, loader
from view_helpers import View
    
class GameView(View):
    def __call__(self, request, *args, **kwargs):
        if 'computer_first' in kwargs:
            option_string = kwargs.pop('computer_first')
            if option_string == 'True':
                self.computer_first = True
            else:
                self.computer_first = False
        else:
            self.computer_first = True
            #TODO return improper args page here
            pass
        
        self.context = {
            'computer_first': self.computer_first
        }
        return super(GameView, self).__call__(request, *args, **kwargs)

    def get(self):
        
        return self.render()
    
    def render(self):
        return render_to_response('game/game.html', 
                                  self.context, 
                                  context_instance=RequestContext(self.request))