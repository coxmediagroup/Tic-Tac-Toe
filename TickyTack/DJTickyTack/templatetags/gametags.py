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

    def renderCell(self, ttt, r, c, value, editable):
        if value in ('X', 'O') or not editable:
            cssClass = 'empty' if value == '_' else value
            return '<td class="%s">%s</td>' % (cssClass, value)
        else:
            move = ttt.toPlay + 'ABC'[c] + '123'[r]
            return ''.join(
            [
                '<td class="%s">',
                ' <input type="radio" name="move" value="%s"/>' % move,
                '</td>'
            ])

    def genBoard(self, game, editable):
        t = game.asTicTacToe()
        yield '<div class="%s">' % self.cssClass
        yield '<table onclick="%s">' % self.onClick(game)
        for r, row in enumerate(game.asGrid()):
            yield '<tr>'
            for c, cell in enumerate(row):
                yield self.renderCell(t, r, c, cell, editable)
            yield '</tr>'
        yield '</table>'
        yield '<div class="VsString"><a href="%s">%s</a></div>' % (
            game.asUrl(), game.asVsString())
        yield '</div>'

    def render(self, context):
        game = context[self.gameVar]
        editable = self.editable and game.toPlay == context['user']
        return ''.join(self.genBoard(game, editable))

    def onClick(self, game):
        return ''



class GameBadgeNode(GameBoardNode):

    def __init__(self, gameVar):
        super(GameBadgeNode, self).__init__(gameVar)
        self.cssClass = "GameBadge"
        self.editable = False

    def onClick(self, game):
        return 'document.location=%s' % repr(game.asUrl())