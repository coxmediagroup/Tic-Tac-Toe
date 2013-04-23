from django.template import loader
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from forms import UserForm


def user_registration(request):
    form_message = None

    if request.user.is_authenticated():
        return HttpResponseRedirect('/tictactoe/play')

    if request.method == 'POST': # If the form has been submitted...

        user_form = UserForm(request.POST)

        if user_form.is_valid(): # All validation rules pass
            new_user = User.objects.create_user(
                user_form.cleaned_data['username'],
                user_form.cleaned_data['email'],
                user_form.cleaned_data['password']
            )
            new_user.first_name = user_form.cleaned_data['first_name']
            new_user.last_name = user_form.cleaned_data['last_name']
            new_user.save()

            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'])
            login(request, user)

            # analytics_event = Event(
            #                     event_type='DOULA_REGISTERED',
            #                     event_url=request.path,
            #                     event_model=new_doula.__class__.__name__,
            #                     event_model_id=new_doula.id
            #                 )
            # analytics_event.save()

            return HttpResponseRedirect('/tictactoe/play') # Redirect after POST

        else:
            form_message = ('There are errors in some form fields, please fix '
            'them and resubmit.')

    else:
        user_form = UserForm()

    template = loader.get_template('registration.html')
    context = RequestContext(
        request,
        {
            'form_message': form_message,
            'registration_form': user_form,
        }
    )
    return HttpResponse(template.render(context))
