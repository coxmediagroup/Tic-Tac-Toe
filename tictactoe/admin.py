from django.contrib import admin

from . import models

class MoveInline(admin.TabularInline):
    model = models.Move
    readonly_fields = ('created', 'cell',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class GameAdmin(admin.ModelAdmin):
    list_display = ['created', 'ip', 'player', 'winner']
    inlines = [MoveInline]

    readonly_fields = ('created', 'player', 'winner', 'steps')

    fieldsets = (
        (None, {
            'fields':('created', 'player', 'winner', 'steps')
        }),
    )

    def steps(self, game=None):
        if game is None:
            return ''
        else:
            steps = []
            move_list = game.move_list().split('-')
            for i in xrange(len(move_list)):
                s = ['<div class="tic-tac-toe-step">']

                board = {}
                for r in '123':
                    for c in 'ABC':
                        board[c+r] = '<div></div>'


                turn = 'X'
                for j in xrange(i):
                    board[move_list[j]] = '<div>%s</div>' % turn
                    turn = 'O' if turn == 'X' else 'X'

                board[move_list[i]] = '<div class="tic-tac-toe-move">%s</div>' % turn

                for r in '123':
                    s.append('<div>')
                    for c in 'ABC':
                        s.append(board[c+r])
                    s.append('</div>')

                s.append('</div>')
                steps.append(''.join(s))

            return '<div class="tic-tac-toe-sequence">' + ''.join(steps) + '</div>'
    steps.allow_tags = True

    def has_add_permission(self, request):
        return False

admin.site.register(models.Game, GameAdmin)
