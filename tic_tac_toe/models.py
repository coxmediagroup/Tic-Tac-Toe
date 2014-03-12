from django.db import models

# Create your models here.

class Entity(models.Model):
    is_ai = models.BooleanField(default=False)

    def get_type(self):
        # get a human-readable string of this entity's type
        #    this should be either "Human" or "Computer"
        #    this could possibly be expanded to be a player's name
        if self.is_ai:
            return 'Computer'
        return 'Human'

    def get_decision(self):
        # get a decision from either the human or the ai
        #    this may need to change as I figure out django
        if(self.get_type() == 'Human'):
            pass
        else:
            pass
        pass

class Game(models.Model):
    current_player = models.ForeignKey(Entity)

    def get_location(self, x, y):
        # get the location object of the given location
        pass
class Board(models.Model):
    game = models.ForeignKey(Game)

class Row(models.Model):
    board = models.ForeignKey(Board)
    row = models.IntegerField()

class Location(models.Model):
    column = models.IntegerField()
    row = models.ForeignKey(Row)
    occupier = models.ForeignKey(Entity)

    def claim(self, entity_id):
        # set the occupier of this field to the given entity id
        pass

