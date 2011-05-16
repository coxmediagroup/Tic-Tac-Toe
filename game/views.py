# Create your views here.
from models import BoardError, Board, Player, ComputerPlayer

from django import forms
from django.shortcuts import render, redirect

MARKER_CHOICES = (("X", "X"), ("O", "O"),)
MOVE_CHOICES = (("1","1"),("2","2"),("3","3"),("4","4"),("5","5"), ("6","6"), ("7","7"), ("8","8"), ("9","9"), ("C", "C"),)

class IntroForm(forms.Form):

    name = forms.CharField(label="Please enter your name:")
    marker = forms.ChoiceField(label= "Select which marker you would like to use:", choices = MARKER_CHOICES)

class MoveForm(forms.Form):
    move = forms.ChoiceField(label= "Select which area to place marker: ", choices=MOVE_CHOICES)

def index(request):
    params = {}
    session = request.session
    if request.method == 'POST':
        form = IntroForm(request.POST)
        if form.is_valid():
            board = Board()
            marker = form.cleaned_data["marker"]
            name = form.cleaned_data["name"]
            session["player"] = Player(marker, board, name)
            if marker == "X":
                computer_marker = "O"
            else:
                computer_marker = "X"
            session["computer"] = ComputerPlayer(computer_marker, board)
            session["board"] = board
            return redirect("board")
    else:
        form = IntroForm()
    params["form"] = form
    return render(request, "index.html", params )

def board(request):
    session = request.session
    board = session["board"]
    player = session["player"]
    computer = session["computer"]
    params = {}
    if request.method == "POST":
        form = MoveForm(request.POST)
        if form.is_valid():
            index = form.cleaned_data["move"]
            if index.isdigit():
                player.place_marker(int(index) -1)
                if board.winner == None:
                    computer.place_marker()
            else:
                board.declare_cat()
    else:
        form = MoveForm()
    session["board"] = board
    session["player"] = player
    session["computer"] = computer
    params["board"] = board
    params["form"] = form
    return render(request, "board.html", params)
