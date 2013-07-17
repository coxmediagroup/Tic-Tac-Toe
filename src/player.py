import sys

class Player(object):
    def __init__(self, board, first):
        self._board = board
        self._first = first

        # Set the mark used by this player (player who goes first is
        # always 'X' -- official rules)
        self.mark = ["O", "X"][first]

    def _setmark(self, pos):
        self._board.setmark(pos, self._name, self.mark)

    def turn(self):
        print >> sys.stderr, "need to override turn()"
        sys.exit(1)

class Computer(Player):
    def __init__(self, board, first):
        super(Computer, self).__init__(board, first)
        self.__winning = [False, True][first]   # Set to True if first player, False otherwise
        self._name = "Computer"

    def turn(self):
        # Given experience players, there is a sneaky way to win.  If we have
        # the following scenario:
        #
        #   1) 1st player puts his mark in a corner on 1st turn
        #   2) 2nd player puts his mark in center on 1st turn
        #   3) 1st player puts his mark in opposite corner on 2nd turn
        #   4) 2nd player puts his mark in any empty corner on 2nd turn
        #
        # then 1st player can win.  We don't have to worry if the human tries
        # to do that to us since the alternative strategy will defeat it.
        #
        # The alternative strategy is to first check to see if we can win.  If
        # not, then we check if the human has a winning position and to block that.
        # If not, try to find the best position we can.

        if self.__winning:
            # We will try the ONLY chance of winning strategy

            if self._board.numturn == 1:
                # First turn, mark a corner
                self._setmark(0)
            elif self._board.numturn == 3:
                # Second turn, if human put a mark in the center,
                # continue with the winning strategy.  Otherwise
                # follow through on the normal strategy

                if not self._board.is_empty(4):
                    self._setmark(8)
                else:
                    self.__winning = False
            else:
                # If the first 2 steps were done, we don't need to check
                # anymore as the normal strategy will work to complete the
                # winning strategy as part of it's normal course.  If the first
                # two steps weren't done, then we need to switch strategy
                # anyway.

                self.__winning = False

        # Can't do this as an 'else' to the IF statement above since the status
        # could chance within that statement and we would need to do this
        # anyway.
        if self.__winning == False:
            # Execute the alternative strategy

            # If we can win, do it now
            pos = self._board.match_nummarks(self.mark, 2)
            if len(pos):
                self._setmark(pos[0])
            else:
                # Get list of winning positions for Human
                win_pos = self._board.match_nummarks(["X", "O"][self._first], 2)

                if len(win_pos):
                    # Human can win, must block
                    self._setmark(win_pos[0])
                else:
                    self._setmark(self.__bestpos())

    def __bestpos(self):
        """Find the best position to mark"""

        # The best position would be if there are already 2 computer marks in a
        # row, column, or diagonal and the third space is empty.  If not, we go
        # for center.  If center isn't available, we just go for the first
        # available empty space.

        pos = self._board.match_nummarks(self.mark, 2)

        if len(pos):
            return pos[0]

        # Go for center
        if self._board.is_empty(4):
            return 4

        # Find the first available empty space
        for pos in xrange(9):
            if self._board.is_empty(pos):
                return pos

class Human(Player):
    def __init__(self, board, first):
        super(Human, self).__init__(board, first)
        self._name = "Lowly Human"

    def turn(self):
        print

        # Show the board if going first
        if self._first and self._board.numturn == 1:
            self._board.draw()
            print

        print "It's your turn.  Enter the value of the position to put an '%c'." % self.mark

        # Keep asking for a space to mark until we get a valid answer
        while True:
            try:
                choice = raw_input("Position? ")

                try:
                    # Make sure answer is an integer value
                    choice = int(choice) - 1

                    # Make sure answer is in the valid range of choices
                    if choice < 0 or choice > 8:
                        print "Not a valid choice, try again"
                        continue

                    # Make sure answer is an empty space
                    if self._board.is_empty(choice):
                        self._setmark(choice)
                        break
                    else:
                        print "Position already has a mark, try again"
                        continue
                except ValueError:
                    print "Not a valid choice, try again"
                    continue
            except (EOFError, KeyboardInterrupt):
                print "\n\nI see you want to quit.  Computer wins by default."
                sys.exit(0)

