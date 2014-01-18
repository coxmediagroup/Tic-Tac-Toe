
from django import template

register = template.Library()

@register.simple_tag
def board_cell(board, row, col):
    """ translates a board cell to a fontawesome class value """
    return board.cell_class(row=row, col=col)

