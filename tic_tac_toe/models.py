from django.db import models

# Create your models here.

class Game(models.Model):
    current_player = models.ForeignKey('Entity', null=True, related_name='+')

    def get_location(self, x, y):
        # get the location object of the given location
        pass

    def setup_new_game(self):
        self.save()

        # 1 entity for the player, 1 for the computer
        human = Entity(is_ai=False, game=self)
        ai = Entity(is_ai=True, game=self)

        # save what we have so far
        human.save()
        ai.save()

        # ai starts
        self.current_player = ai #TODO: randomize starting order
        self.save()

        board = Board(game=self)
        board.save()

        # create a 3x3 grid, saving each object along the way
        for i in range(3):
            row = Row(row=i, board=board)
            row.save()
            for i in range(3):
                loc = Location(column=i, row=row)
                loc.save()

class Entity(models.Model):
    is_ai = models.BooleanField(default=False)
    game = models.ForeignKey(Game)

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


class Board(models.Model):
    game = models.ForeignKey(Game)

class Row(models.Model):
    board = models.ForeignKey(Board)
    row = models.IntegerField()

class Location(models.Model):
    column = models.IntegerField()
    row = models.ForeignKey(Row)
    occupier = models.ForeignKey(Entity, null=True)

    def claim(self, entity_id):
        # set the occupier of this field to the given entity id
        #TODO: how do I get an entity by its index?
        pass
