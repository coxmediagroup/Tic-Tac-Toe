"""
Custom tags for rendering tic tac toe games.
"""
from django import template
from django.template import Node

register = template.Library()


@register.tag
def game_board(parser, token):
    tag, gameVar = token.split_contents()
    return GameBoardNode(gameVar)

@register.tag
def game_badge(parser, token):
    tag, gameVar = token.split_contents()
    return GameBadgeNode(gameVar)



class GameBoardNode(Node):

    def __init__(self, gameVar):
        self.gameVar = gameVar
        self.cssClass = "GameBoard"
        self.editable = True

    def renderCell(self, r, c, value):
        if value in ('X', 'O') or not self.editable:
            cssClass = 'empty' if value == '_' else value
            return '<td class="%s">%s</td>' % (cssClass, value)
        else:
            move = 'ABC'[c] + '123'[r]
            return ''.join(
            [
                '<td class="%s">',
                ' <input type="radio" name="cell" value="%s"/>' % move,
                '</td>'
            ])

    def genBoard(self, game):
        yield '<div class="%s">' % self.cssClass
        yield '<table>'
        for r, row in enumerate(game.asGrid()):
            yield '<tr>'
            for c, cell in enumerate(row):
                yield self.renderCell(r, c, cell)
            yield '</tr>'
        yield '</table>'
        yield '<div class="VsString"><a href="%s">%s</a></div>' % (
            game.asUrl(), game.asVsString())
        yield '</div>'

    def render(self, context):
        return ''.join(self.genBoard(context[self.gameVar]))



class GameBadgeNode(GameBoardNode):

    def __init__(self, gameVar):
        super(GameBadgeNode, self).__init__(gameVar)
        self.cssClass = "GameBadge"
        self.editable = False
