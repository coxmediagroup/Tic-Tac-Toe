# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import Context, RequestContext, loader
from view_helpers import View
from forms import OptionsForm

class OptionsView(View):
    def __call__(self, request, *args, **kwargs):
    
        return super(OptionsView, self).__call__(request, *args, **kwargs)

    def get(self):
        form = OptionsForm()

        self.context = {
            'form' : form,
            }
        
        return self.render()
        
    #@decorate_method(transaction.commit_on_success)
    def post(self):
        
        form = OptionsForm(self.request.POST)
        
        if form.is_valid():
            return redirect('game', computer_first=form.cleaned_data['computer_first'])
            #print 'valid'
            #return redirect('/game/%s' % form.cleaned_data['computer_first'])
            #print 'after redir'
        else: # validation failed, cant happen in this case
            print 'validation failed'
            pass
        
        self.context = {
            'form' : form,
           }       
        return self.render()    
    
    def render(self):
        return render_to_response('root.html', 
                                  self.context, 
                                  context_instance=RequestContext(self.request))
    
    