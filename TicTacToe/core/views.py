from django.shortcuts import render


def standard(request):
    msg = None
    return render(request, 'grid.html', {'msg': msg})