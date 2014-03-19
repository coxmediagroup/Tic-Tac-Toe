from django.db import models

# Create your models here.
class Game(models.Model):
    board = models.CharField(default="   \n   \n   ", max_length=11)
    game_count = models.PositiveIntegerField(default=1)
    draw_count = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "Board:\n+---+\n|" + ( "|\n|".join(self.board.split("\n")) ) + \
            "|\n+---+\nGame count: " + unicode(self.game_count) + "\nDraw count: " + \
            unicode(self.draw_count) + "\nLast update: " + \
            self.last_update.strftime("%a, %b %m, %Y @ %I:%M:%S %p %Z") + "\n"
