import sys

class Player(object):
    def __init__(self, first):
        self.__first = first

    def turn(self):
        print >> sys.stderr, "need to override turn()"
        sys.exit(1)

class Computer(Player):
    pass

class Human(Player):
    pass

