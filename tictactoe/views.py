from django.shortcuts import render


def say_hello(request):
    """A hello-world test view."""

    game_board = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    return render(request, "tictactoe/hello.html.djt", {'board': game_board})