from django.db import models
from django.contrib import admin

class Game(models.Model):
    pass

class GameAdmin(admin.ModelAdmin):
    pass

class Play(models.Model):
    game = models.ForeignKey(Game)

class PlayAdmin(admin.ModelAdmin):
    list_display = ["game"]
    
admin.site.register(Play, PlayAdmin)
admin.site.register(Game, GameAdmin)