import sys

class Player(object):
    def __init__(self, board, first):
        self.__board = board
        self.__first = first

        # Set the mark used by this player (player who goes first is
        # always 'X' -- official rules)
        self.mark = ["O", "X"][first]

    def turn(self):
        print >> sys.stderr, "need to override turn()"
        sys.exit(1)

class Computer(Player):
    pass

class Human(Player):
    pass

