import random


class GameTile:
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


class GameBoard:
    """
    Manages the current game state
    """
    _BOARD_SIZE = 3
    _COMPUTER = 'x'
    _PLAYER = 'o'

    def __init__(self):
        # generate the tile set
        self.tiles = [[GameTile(x, y) for y in range(GameBoard._BOARD_SIZE)] for x in range(GameBoard._BOARD_SIZE)]
        self.winner = None

        # winning combos only need to be defined once at the beginning of the game
        self.winning_combos = [col for col in self.tiles] + \
                              [[col[i] for col in self.tiles] for i in range(GameBoard._BOARD_SIZE)] + \
                              [[self.tiles[i][i] for i in range(GameBoard._BOARD_SIZE)]] + \
                              [[self.tiles[i][GameBoard._BOARD_SIZE - i - 1] for i in range(GameBoard._BOARD_SIZE)]]

        # determine starting player and play if the computer starts
        if random.choice([GameBoard._PLAYER, GameBoard._COMPUTER]) == GameBoard._COMPUTER:
            #TODO: call the function to trigger computer move
            pass

    @property
    def available_tiles(self):
        available = []

        #TODO: this can be cleaner, try list a comprehension
        #[row for row in col for col in self.tiles if not row.value]
        for col in self.tiles:
            for row in col:
                if not row.value:
                    available.append(row)
        return available

    def check_winner(self):
        # determine if there is a winner for the game right now
        winner = reduce(lambda x, y: x or y, [combo[0].value for combo in self.winning_combos
                                              if all(combo[0].value == tile.value for tile in combo[1:])])

        # winner is either a player, none, or some other value that represents a draw
        if not winner and not self.available_tiles:
            # no winner and no moves left?  it's a cats game
            # TODO: define a value to represent a draw
            return None
        return winner