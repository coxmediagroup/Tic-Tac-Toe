from django.core.exceptions import ValidationError
import re

def is_x_or_o(v):
    if v not in 'XO':
        raise ValidationError('Should be either X or O')

def is_cell(v):
    if not re.search(r'^[A-C][1-3]$', v):
        raise ValidationError('Should be a cell (e.g. "A1" or "B2")')
