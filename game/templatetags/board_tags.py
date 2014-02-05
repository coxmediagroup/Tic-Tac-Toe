from django import template
from django.conf import settings

url = settings.STATIC_URL

register = template.Library()

@register.simple_tag
def render_board(board):
    str = "<table>"
    if board.winner != None:
        str += "<tr><td colspan='3' align='center'><h3>Winner is {0}</h3></td></tr>".format(board.winner)
    str += "<tr>"
    counter = 0
    for ele in board.grid:
        body = ele
        if body == None:
            body = "blank"
        str += "<td><img src='{0}{1}.jpg' width='150px' /></td>".format(url, body)
        counter += 1
        if counter % 3 == 0:
            str +="</tr><tr>"
    str += "</table>"
    return str

