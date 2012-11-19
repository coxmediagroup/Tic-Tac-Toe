from django.contrib import admin

from .models import Game


class GameAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('grid', 'created')
    list_filter = ('created', 'modified')
    readonly_fields = ('created', 'modified')

    # TODO: Add method to output grid as HTML table in ``list_display``.


admin.site.register(Game, GameAdmin)
