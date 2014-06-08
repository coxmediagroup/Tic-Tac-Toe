from django.shortcuts import render
from django import forms

from .game import GameBoard

def index(request):
   if request.method == "POST":
      move_form = SubmitMoveForm(request.POST)
      
      state = move_form['state'].value()
      row = int(move_form['row'].value())
      column = int(move_form['column'].value())
      
      game_board = GameBoard(state)
      game_board.move(row, column)
   else:
      game_board = GameBoard()

   return render(request, 'board.html', {'game': game_board})
      
      
class SubmitMoveForm(forms.Form):
    row = forms.IntegerField(min_value=0, max_value=2)
    column = forms.IntegerField(min_value=0, max_value=2)
    state = forms.CharField(min_length=9, max_length=9)
    