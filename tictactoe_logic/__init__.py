"""AI and win condition detection functions for Tic-tac-toe .

For all functions, a ``board`` parameter is expected to be a list of three
strings, all three characters long, where any character is either
- ' ' for a blank cell
- 'X' for a cell taken by X
- 'O' for a cell taken by O

"""

from .ai import get_ai_move

__all__ = ['get_ai_move']