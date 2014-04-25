from django.shortcuts import render


def say_hello(request):
    """A hello-world test view."""
    return render(request, "tictactoe/hello.html.djt", {'msg': 'From Django'})