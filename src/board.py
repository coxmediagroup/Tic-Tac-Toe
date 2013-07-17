class Board(object):
    def __init__(self):
        # Board spaces will be represented by a list.  This list
        # shows where the players have a mark or a space is empty.
        # Indices relate to the board as follows:
        #
        #                0 | 1 | 2
        #               ---|---|---
        #                3 | 4 | 5
        #               ---|---|---
        #                6 | 7 | 8

        self.spaces = [False for index in xrange(9)]

    def draw(self):
        self.__drawrow(0, 3)
        print "\t ---|---|---"
        self.__drawrow(3, 6)
        print "\t ---|---|---"
        self.__drawrow(6, 9)

    def __drawrow(self, start, end):
        print "\t ",

        for index in xrange(start, end):
            mark = [str(index + 1), self.spaces[index]][self.spaces[index]]

            print "%s" % mark,

            if index < (end - 1):
                print "|",

        print

