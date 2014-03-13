from django.db import models


class Game(models.Model):
    # should be 1 or 2 to indicate first or second player
    current_player = models.IntegerField(default=2)

    player_one = models.ForeignKey('Entity', null=True, related_name='+')
    player_two = models.ForeignKey('Entity', null=True, related_name='+')

    def next_player(self):
        self.current_player = (2 if self.current_player == 1 else 1)
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
        for row_i in range(3):
            row = Row(row=row_i, board=board)
            row.save()
            for col_i in range(3):
                loc = Location(column=col_i, row=row)
                loc.save()

    def get_win_scenarios(self):
        possibles = [
            # left-down diagonal
            (
                (0, 0),
                (1, 1),
                (2, 2),
            ),
            # right-down diagonal
            (
                (0, 2),
                (1, 1),
                (2, 0),
            ),
        ]

        # horizontals
        for i in range(3):
            possibles.append((
                (i, 0),
                (i, 1),
                (i, 2),
            ))
        # verticals
        for i in range(3):
            possibles.append((
                (0, i),
                (1, i),
                (2, i),
            ))
        return possibles

    def get_winner(self):
        moves_available = False
        possibles = self.get_win_scenarios()
        for streak in possibles:
            # resolve a streak to its occupiers
            occupiers = [self.get_location(*coords).occupier for coords in streak]
            if occupiers[0] != None and occupiers.count(occupiers[0]) == 3:
                # if all three cells in this streak are the same, it's a winner
                return '%s Wins!'%(occupiers[0].get_type(),)

            elif None in occupiers:
                # if one of the cells is empty, make note
                moves_available = True

        if not moves_available:
            # if we didn't find any empty cells, we must have a draw
            return "It's a Draw!"

        return None


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

    def get_decision(self):
        game = self.game

        choice_location = game.get_location(0, 0)
        if choice_location.occupier is None:
            # this will never fail if the ai does not occupy the space
            #    because the ai goes first
            pass # we'll claim it in a bt
        else:
            # check for possible wins
            possibles = game.get_win_scenarios()

            immediate_wins = []
            immediate_losses = []
            possible_losses = []
            for possible in possibles: # go through possible win scenarios
                # get status of each cell in the scenario
                results = [game.get_location(*cell).occupier for cell in possible]

                if results.count(self) == 2 and results.count(None) == 1:
                    # we have a winner, claim the cell
                    immediate_wins.append(possible[results.index(None)])

                elif results.count(self) == 0 and results.count(None) == 1:
                    # we have an imminent loss, claim the cell to prevent
                    immediate_losses.append(possible[results.index(None)])

                elif results.count(self) == 0:
                    # we have an possible loss, claim the cell to prevent
                    possible_losses.append(possible[results.index(None)])

            if immediate_wins:
                choice_location = game.get_location(*immediate_wins[0])
            elif immediate_losses:
                choice_location = game.get_location(*immediate_losses[0])
            elif possible_losses:
                choice_location = game.get_location(*possible_losses[0])
            else:
                # if we've gotten here, we have a claim in each possible
                #   loss route, so we can just pick a random cell
                choice_location = None
                for row_i in range(3):
                    for col_i in range(3):
                        possible_location = game.get_location(row_i, col_i)
                        if possible_location.occupier is None:
                            choice_location = possible_location
                            break
                    if choice_location:
                        break

        # claim whatever cell we wound up on
        choice_location.claim(self)

        choice_location.save()
        game.next_player()



class Board(models.Model):
    game = models.ForeignKey(Game)


class Row(models.Model):
    board = models.ForeignKey(Board)
    row = models.IntegerField()


class AlreadyOccupied(Exception):
    pass
class Location(models.Model):
    column = models.IntegerField()
    row = models.ForeignKey(Row)
    occupier = models.ForeignKey(Entity, null=True)

    def claim(self, entity):
        # set the occupier of this field to the given entity
        if self.occupier is None:
            self.occupier = entity
        else:
            raise AlreadyOccupied('The given location is already occupied!')
