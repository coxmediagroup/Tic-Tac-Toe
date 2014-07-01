import random


class GameTile (object):
    """
    Manages the current game tile at the specified x, y position on the board.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = None

    def __unicode__(self):
        return "[GameTile %s, %s: %s]" % (self.x, self.y, self.value)

    def __str__(self):
        return unicode(self).encode('utf-8')


class GameBoard (object):
    """
    Manages the current game state
    """
    _board_size = 3
    _computer = 'x'
    _player = 'o'
    _cats_game = 'cat'

    def __init__(self):
        # generate the tile set
        self.tiles = [[GameTile(x, y) for y in range(GameBoard._board_size)] for x in range(GameBoard._board_size)]
        self.winner = None

        # winning combos only need to be defined once at the beginning of the game after the tiles are generated
        self.winning_combos = [col for col in self.tiles] + \
                              [[col[i] for col in self.tiles] for i in range(GameBoard._board_size)] + \
                              [[self.tiles[i][i] for i in range(GameBoard._board_size)]] + \
                              [[self.tiles[i][GameBoard._board_size - i - 1] for i in range(GameBoard._board_size)]]

        # determine starting player and play if the computer starts
        if random.choice([GameBoard._player, GameBoard._computer]) == GameBoard._computer:
            #TODO: call the function to trigger computer move
            pass

    @property
    def available_tiles(self):
        """ Return a list of all tiles that have not been used """
        return [row for col in self.tiles for row in col if not row.value]

    def check_winner(self):
        """
        Determine if there is currently a winner. Should only be called after a valid move is made.
        """
        winner = reduce(lambda x, y: x or y, [combo[0].value for combo in self.winning_combos
                                              if all([combo[0].value == tile.value for tile in combo[1:]])])

        if not winner and not self.available_tiles:
            # no winner and no moves left?  it's a cat's game
            return GameBoard._cats_game
        return winner

    def player_move(self, x, y):
        """
        Update the the game board when the user plays a tile and check for a winner
        """
        tile = self.tiles[x][y]
        if tile.value:
            # that tile has already been taken
            # TODO: notify the user that they made an illegal move
            return

        tile.value = GameBoard._player
        self.winner = self.check_winner()
        return self.winner

    def computer_move(self):
        """
        Make the computer perform a valid move and check for a winner
        """