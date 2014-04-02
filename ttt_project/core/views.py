from django.shortcuts import render
from annoying.decorators import render_to

@render_to('core/core.html')
def main(request):
    return {}
