from django.db import models

# Create your models here.


class Move(models.Model):
  session_id = models.CharField(max_length=36)
  insert_id = models.AutoField(primary_key=True)
  player = models.CharField(max_length=1)
  position = models.IntegerField()


