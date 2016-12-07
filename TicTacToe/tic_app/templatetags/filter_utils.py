from django.template import Library
register = Library()

#returns the range of the given number
@register.filter
def get_range( value ):
    return range(value)

#returns corresponding character of input
@register.filter
def get_char(value):
    return chr(int(value)).upper()

#returns a%b
@register.filter
def modulo(a,b):
    return a % b