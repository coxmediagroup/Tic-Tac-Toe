from django.db import models

class Game(models.Model):

    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%d:%s" % (self.pk, self.name)