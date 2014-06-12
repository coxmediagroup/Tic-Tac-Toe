from django.shortcuts import render
from django import forms

import random

from .game import GameBoard
from .player import *

def index(request, player=GameBoard.player_x):
   if request.method == "POST":
      move_form = SubmitMoveForm(request.POST)
      
      state = move_form['state'].value()
      row = int(move_form['row'].value())
      column = int(move_form['column'].value())
      
      game_board = GameBoard(state)
      game_board.move(row, column)
      
      if game_board.is_game_over():
         return render(request, 'end.html', {'game': game_board})
         
      game_board.move(*PlayerMinimax.choose_move(game_board))
      
      if game_board.is_game_over():
         return render(request, 'end.html', {'game': game_board})
         
   else:
      game_board = GameBoard()
      
      if player == GameBoard.player_o:
         game_board.move(*random.choice(game_board.get_valid_moves()[:5]))

   return render(request, 'board.html', {'game': game_board})
      
class SubmitMoveForm(forms.Form):
    row = forms.IntegerField(min_value=0, max_value=2)
    column = forms.IntegerField(min_value=0, max_value=2)
    state = forms.CharField(min_length=9, max_length=9)
    