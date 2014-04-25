"""AI and win condition detection functions for Tic-tac-toe .

For all functions, a ``board`` parameter is expected to be a list of strings,
where any character in any string is either ' ' for a blank cell, 'X' for a
cell taken by X, and 'O' for a cell taken by O.

"""
from .logic import get_ai_move

__all__ = ['get_ai_move']