"""
Game logic code module.

"""

from copy import deepcopy

class Board:
    """
    Board objected, needed for AI to be able to maintain multiple boards.

    A game can have multiple boards, because the AI will sometimes create
    boards to consider moves.

    """

    def __init__(self, setup=None):
        self._board = {}
        if not setup:
            for x in range(0, 3):
                self._board[x] = {}
                for y in range(0, 3):
                    self._board[x][y] = " "
        else:
            self._board = deepcopy(setup)

    def board(self):
        """
        Show the current state of the board.

        """

        return self._board

    def square(self, coords, set_to=None):
        """
        Look up the symbol at the specified coords.

        coords can be a list or tuple: (x, y)

        """
        if not set_to:
            return self._board[coords[0]][coords[1]]
        else:
            self._board[coords[0]][coords[1]] = set_to

    def move(self, coords, symbol, test=False):
        """
        Add a new symbol to the board.
        returns True if move is valid, False otherwise.

        test: if test=True, copy the board, make the move,
              and return the board for viewing.

        """

        if self.square(coords) == " ":
            self.square(coords, set_to=symbol)
            if test:
                return self
            return True
        return False

    def check_requirements(self, pathway, requires):
        """
        Check a pathway against the stated requirements.

        """
        contents = {}
        for e in pathway:
            val = self.square(e)
            if val not in contents.keys():
                contents[val] = 1
            else:
                contents[val] += 1

        for e in requires.keys():
            try:
                if contents[e] < requires[e]:
                    return False
            except KeyError:
                return False

        return True

    def traverse(self, banned=None, requires=None):
        """
        Traverse the board and return the eight different pathways
        as a list of lists.

        banned: ignore pathways if they contain these symbols
        requires: {"X": 3}, etc.  {symbol, required number}

        """
        banned = [] if banned == None else banned
        requires = {} if requires == None else requires

        minimum = 3
        paths = []

        # rows
        for row in range(0, 3):
            pathway = []
            for col in range(0, 3):
                if False and self.square((row, col)) in banned:
                    continue
                else:
                    pathway.append((row, col))

            if(len(pathway) >= minimum
                    and self.check_requirements(pathway, requires)):
                paths.append(pathway)

        # columns
        for col in range(0, 3):
            pathway = []
            for row in range(0, 3):
                if False and self.square((row, col)) in banned:
                    continue
                else:
                    pathway.append((row, col))

            if(len(pathway) >= minimum
                    and self.check_requirements(pathway, requires)):
                paths.append(pathway)

        # diagonals
        pathway = []
        for row in range(0, 3):
            col = row # diagonal magic
            if False and self.square((row, col)) in banned:
                continue
            else:
                pathway.append((row, col))

        if(len(pathway) >= minimum
                and self.check_requirements(pathway, requires)):
            paths.append(pathway)

        pathway = []
        # Need to consider the other diagonal.  Subtracting
        # 2 and taking the absolute value yields the
        # appropriate numbers.
        for row in range(0, 3):
            col = abs(row - 2)
            if False and self.square((row, col)) in banned:
                continue
            else:
                pathway.append((row, col))

        if(len(pathway) >= minimum
                and self.check_requirements(pathway, requires)):
            paths.append(pathway)

        return paths

    def is_draw(self):
        """
        See if the game is a draw.

        """

        open_spaces = self.traverse(requires={" ": 1})
        if not open_spaces:
            return 'True'

        return 'False'

    def is_win(self):
        """
        See if the game is a winner, returning the winner if there is one,
        or an empty string if not.

        """
        x_wins = self.traverse(requires={"X": 3})
        o_wins = self.traverse(requires={"O": 3})

        return 'player' if x_wins else 'ai' if o_wins else ''


