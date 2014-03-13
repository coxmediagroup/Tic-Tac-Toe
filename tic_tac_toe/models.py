from django.db import models

# Create your models here.

class Game(models.Model):
    # should be 1 or 2 to indicate first or second player
    current_player = models.IntegerField(default=2)

    player_one = models.ForeignKey('Entity', null=True, related_name='+')
    player_two = models.ForeignKey('Entity', null=True, related_name='+')

    def next_player(self):
        self.current_player = '2' if self.current_player == '1' else '1'
        self.save()

    def get_location(self, row_id, col_id):
        # get the location object of the given location
        board = self.board_set.first()
        row = board.row_set.get(row=row_id)
        location = row.location_set.get(column=col_id)
        return location

    def setup_new_game(self):
        self.save() # save so that we get a primary key

        # 1 entity for the player, 1 for the computer
        human = Entity(is_ai=False, game=self, symbol='X')
        ai = Entity(is_ai=True, game=self, symbol='O')

        # save what we have so far
        human.save()
        ai.save()

        # set entities as players
        self.player_one = human
        self.player_two = ai

        # ai starts
        self.current_player = 2 #TODO: randomize starting order

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
    symbol = models.CharField(max_length=1)

    def get_type(self):
        # get a human-readable string of this entity's type
        #    this should be either "Human" or "Computer"
        #    this could possibly be expanded to be a player's name
        if self.is_ai:
            return 'Computer'
        return 'Human'

    def get_decision(self, decision_tree=None):
        game = self.game

        # for the first move, take the bottom left corner
        choice_location = game.get_location(0,0)
        if choice_location.occupier == None:
            # this will never fail if the ai does not occupy the space
            #    because the ai goes first
            choice_location.occupier = self
        else:
            # check for possible wins
            possibles = []

            # check the left-down diagonal
            possibles.append((
                (0, 0),
                (1, 1),
                (2, 2),
                ))
            # check the right-down diagonal
            possibles.append((
                (0, 2),
                (1, 1),
                (2, 0),
                ))
            # check horizontals
            for i in range(3):
                possibles.append((
                    (i, 0),
                    (i, 1),
                    (i, 2),
                    ))
            # check verticals
            for i in range(3):
                possibles.append((
                    (0, i),
                    (1, i),
                    (2, i),
                    ))

            break_out = False # a variable that when true will cause the
                              #    successive checks to halt
            for possible in possibles: # go through possible win scenarios
                # get status of each cell in the scenario
                results = [game.get_location(*cell).occupier for cell in possible]
                # if ai owns 2 cells, and there's an empty, just claim the empty
                if results.count(self) == 2 and results.count(None) == 1:
                    # we have a winner, figure out which one is empty and take it
                    continue # TODO: figure out which cell to claim and claim it
                    break_out = True
                    break
            # if we didn't find a winnable scenario, get into the hairy bits of
            #   figuring out what the next best option is
            if not break_out:
                # check for immediate losses
                for possible in possibles: # go through possible win scenarios
                    # get status of each cell in the scenario
                    results = [game.get_location(*cell).occupier for cell in possible]
                    # if ai owns 0 cells, and there's 1 empty, just claim the empty
                    if results.count(self) == 0 and results.count(None) == 1:
                        # we have an immenent loss, figure out which one is empty and take it
                        continue # TODO: figure out which cell to claim and claim it
                        break_out = True
                        break
                # check for possible losses
                if not break_out:
                    # check for immediate losses
                    for possible in possibles: # go through possible win scenarios
                        # get status of each cell in the scenario
                        results = [game.get_location(*cell).occupier for cell in possible]
                        # if ai owns 0 cells, and there's 1 empty, just claim the empty
                        if results.count(self) == 0:
                            # we have an possible loss, figure out which one is empty and take it
                            continue # TODO: figure out which cell to claim and claim it
                            break_out = True
                            break
                    if not break_out:
                        # if we've gotten here, we have a claim in each possible
                        #   loss route, so we can just pick a random cell
                        pass


        choice_location.save()
        game.next_player()



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
