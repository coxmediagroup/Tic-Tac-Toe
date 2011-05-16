from django import template

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
        str += "<td><img src='/static/{0}.jpg' width='150px' /></td>".format(body)
        counter += 1
        if counter % 3 == 0:
            str +="</tr><tr>"
    str += "</table>"
    return str

