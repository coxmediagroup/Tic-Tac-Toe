from django.template import loader
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import UserForm
from analytics.models import Event
from communications.communications import EmailCommunication


def user_registration(request):
    """
    Provide user registration form and process completed forms.

    In typical Django fashion, this view provides and processes a single
    form.  In this case, a user registration form.

    """

    # Redirect user to game if already logged in.
    if request.user.is_authenticated():
        return HttpResponseRedirect('/tic_tac_toe/game')

    form_message = None

    # User has submitted the form.
    if request.method == 'POST':
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

            analytics_event = Event(
                event_type='USER_REGISTRATION_FINISH',
                event_url=request.path,
                event_model=new_user.__class__.__name__,
                event_model_id=new_user.id
            )
            analytics_event.save()

            email_message = EmailCommunication(
                'grand-chiefain-of-the-moose-people@RGamesR2Smart4U.com',
                [new_user.email],
                '//Registration Confirmation',
                'email/player_registration.html',
                {'first_name': new_user.first_name})
            email_message.send_message()

            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'])
            login(request, user)

            return HttpResponseRedirect('/tic_tac_toe/game')  # Redirect after POST

        else:
            form_message = (
                'There are errors in some form fields, please fix '
                'them and resubmit.')

    # User has not yet submitted the form.
    else:
        user_form = UserForm()

        analytics_event = Event(
            event_type='USER_REGISTRATION_START',
            event_url=request.path,
            event_model=User.__name__
        )
        analytics_event.save()

    template = loader.get_template('registration.html')
    context = RequestContext(
        request,
        {
            'form_message': form_message,
            'registration_form': user_form,
        }
    )
    return HttpResponse(template.render(context))
