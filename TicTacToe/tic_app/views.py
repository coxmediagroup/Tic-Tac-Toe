from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# index view 

@csrf_exempt
def index(request):
    return render(request, 'tic_app/index.html')