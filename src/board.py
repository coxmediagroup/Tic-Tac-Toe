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

        self.__spaces = [False for index in xrange(9)]
        self.numturn = 1

    def draw(self):
        self.__drawrow(0, 3)
        print "\t ---|---|---"
        self.__drawrow(3, 6)
        print "\t ---|---|---"
        self.__drawrow(6, 9)

    def __drawrow(self, start, end):
        print "\t ",

        for index in xrange(start, end):
            mark = [str(index + 1), self.__spaces[index]][self.__spaces[index] != False]

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

    def is_empty(self, pos):
        """Return True if the position is empty, False if filled"""

        return self.__spaces[pos] == False

    def match_nummarks(self, mark, nummarks):
        """Return a list of empty positions given the number of marks to look for"""

        empty_pos = []

        numempties = 3 - nummarks

        # Check rows
        for start in xrange(0, 9, 3):
            self._get_empty_pos(xrange(start, start + 3), mark, nummarks, numempties, empty_pos)

        # Check columns
        for index in xrange(3):
            self._get_empty_pos(xrange(index, 9, 3), mark, nummarks, numempties, empty_pos)

        # Check diagonals
        self._get_empty_pos(xrange(0, 9, 4), mark, nummarks, numempties, empty_pos)
        self._get_empty_pos(xrange(2, 8, 2), mark, nummarks, numempties, empty_pos)

        return empty_pos

    def _get_empty_pos(self, pos_range, mark, nummarks, numempties, empty_pos):
        """Return positions of empty spaces given # marks criteria"""

        filled = []
        empty = []

        for pos in pos_range:
            if self.__spaces[pos] == mark:
                filled.append(pos)
            elif self.__spaces[pos] == False:
                empty.append(pos)

            if len(filled) == nummarks and len(empty) == numempties:
                empty_pos.extend(empty)

    def setmark(self, pos, name, mark):
        """Set a player's mark in the given position.  Return True if
        successful, False otherwise"""

        if self.__spaces[pos] == False:
            print "\n%s places an '%c' in position %d." % (name, mark, pos + 1)

            self.__spaces[pos] = mark
            self.numturn += 1
            return True
        else:
            return False

    def tie(self):
        """Return True if there is a tie game, False if not"""

        empty = filter(lambda value: value == False, self.__spaces)

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

        spaces = self.__spaces

        # Check rows
        for index in xrange(0, 9, 3):
            if spaces[index] != False and \
               spaces[index] == spaces[index + 1] and \
               spaces[index] == spaces[index + 2]:
                return spaces[index]

        # Check columns
        for index in xrange(3):
            if spaces[index] != False and \
               spaces[index] == spaces[index + 3] and \
               spaces[index] == spaces[index + 6]:
                return spaces[index]

        # Check diagonals
        if spaces[0] != False and spaces[0] == spaces[4] and spaces[0] == spaces[8]:
            return spaces[0]

        if spaces[2] != False and spaces[2] == spaces[4] and spaces[2] == spaces[6]:
            return spaces[2]

        return False

