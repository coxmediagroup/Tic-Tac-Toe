from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import TicTacToe


class TicTacToeList(ListView):
    model = TicTacToe


class TicTacToeDetail(DetailView):
    model = TicTacToe

