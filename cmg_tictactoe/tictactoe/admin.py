from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Game, Play


class PlayInline(admin.TabularInline):
    exclude = ('created', 'modified')
    extra = 9
    max_num = 9
    model = Play
    # radio_fields = {'mark': admin.HORIZONTAL}


class GameAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fieldsets = (
        (None, {
            'fields': ('player', 'grid'),
        }),
        (_(u'Auto fields'), {
            'fields': ('created', 'modified'),
            'classes': ('collapse', ),
        }),
    )
    inlines = (PlayInline,)
    list_display = ('player', 'grid', 'created')
    list_filter = ('created', 'modified')
    raw_id_fields = ('player',)
    readonly_fields = ('created', 'modified')
    search_fields = ('player__username', 'player__first_name', 'player__last_name')

    def add_view(self, request, form_url="", extra_context=None):
        """Customized method to prefill new post's author with current user."""
        data = request.GET.copy()
        data['player'] = request.user
        request.GET = data
        return super(GameAdmin, self).add_view(request, form_url=form_url,
                                               extra_context=extra_context)

    # TODO: Add method to output grid as HTML in ``list_display``.


class PlayAdmin(admin.ModelAdmin):
    radio_fields = {'mark': admin.VERTICAL}
    readonly_fields = ('created', 'modified')


admin.site.register(Game, GameAdmin)
admin.site.register(Play, PlayAdmin)
