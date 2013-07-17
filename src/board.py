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

    def endgame(self):
        """We are at the end of the game if we have a winner or tie"""

        # First check if we have a winner
        if self.winner() == False:
            # No winner, check for tie
            return self.tie()
        else:
            return True

    def tie(self):
        """Return True if there is a tie game, False if not"""

        empty = filter(lambda value: value == False, self.spaces)

        # I realize winner() is called twice in rapid succession,
        # once in endgame() and then again here since endgame()
        # calles tie().  If this were a real product and winner()
        # took any real time to run, we would have to optimize
        # so that it wasn't called twice (cache the result from
        # the first time perhaps and/or rearrange the IF statements).
        #
        # This being a simple game and winner() running fast enough
        # not to notice, should I invest the time?  I made the
        # tradeoff (time to code vs speed of execution) to not worry
        # about it.
        #
        # It is still useful to comment about potential problems,
        # and so is documented here.
        return len(empty) == 0 and not self.winner()

    def winner(self):
        """Return the mark of the winner, False if no winner"""

        spaces = self.spaces

        # Check rows
        for index in xrange(0, 9, 3):
            if spaces[index] != False and \
               spaces[index] == spaces[index + 1] and \
               spaces[index] == spaces[index + 2]:
                return True

        # Check columns
        for index in xrange(3):
            if spaces[index] != False and \
               spaces[index] == spaces[index + 3] and \
               spaces[index] == spaces[index + 6]:
                return True

        # Check diagonals
        if spaces[index] != False and \
           ((spaces[0] == spaces[4] and spaces[0] == spaces[8]) or \
            (spaces[2] == spaces[4] and spaces[2] == spaces[6])):
            return True

        return False

