from django.shortcuts import render

# Create your views here.


# index view 
def index(request):
    return render(request, 'tic_app/index.html')