from django.shortcuts import *

def home(request):
    """ Shows main board for current session. """
    return render(request, 'home.django.html', {})