from django.http import HttpResponse

def home_view(request):
    content = 'Hello World!'
    return HttpResponse(content)
