#!/usr/bin/env python2

"""
Game logic code module.
"""

from __future__ import print_function

class Game:
    # List of functions to call when we update the board.
    updates = []
    main_loop = None
    winner = None

    def __init__(self, gui=None):
        import random
        self.board = {}
        for x in range(0, 3):
            self.board[x] = {}
            for y in range(0, 3):
                self.board[x][y] = " "

        self.turn = random.choice(["human", "ai"])
        print("%s's turn." % self.turn)
        self.check_ai_move()

    def move(self, player, x, y):
        """
        Add a move to the game board.
        returns True if move is valid, False otherwise.

        player = "human" or "ai"

        """
        mark = self.get_mark(player)
        # If spot is blank, add, otherwise don't.
        if self.board[x][y] == " ":
            self.board[x][y] = mark
            self.send_update()
            self.next_turn()
            return True
        return False

    def get_mark(self, player):
        """
        Get player's symbol.  (X, or O).

        player = "human" or "ai"

        """
        return "X" if player == "human" else "O"

    def get_board(self):
        return self.board

    def next_turn(self):
        """
        End current turn, start next turn. (changes whose turn it is)

        """
        if not self.turn:
            return
        old = self.turn
        self.turn = "ai" if self.turn != "ai" else "human"
        print("Was %s's turn, now %s's." % (old, self.turn))
        self.check_ai_move()

    def check_ai_move(self):
        """
        See if it's the ai's turn to move, and, if so, move.
        """
        if self.turn == "ai":
            import ai
            valid_move = False
            while not valid_move:
                valid_move = ai.move(self)
            self.send_update()

    def check_for_win(self):
        """
        See if there is a winner.
        """
        winner = None

        paths = self.traverse_board()

        x_wins = self.traverse_board(banned=["O", " "], min=3)
        y_wins = self.traverse_board(banned=["X", " "], min=3)
        winner = x_wins if x_wins else y_wins if y_wins else None
        if winner:
            self.turn = None
            # traverse_board returns paths, and we know each symbol
            # is identical, so grab the first one in the nested list.
            print("Victory: %s" % winner)
            print("Winner: %s" % self.square_lookup(winner[0][0]))

    def square_lookup(self, coords):
        """
        Look up the symbol at the specified coords.

        coords can be a list or tuple: (x, y)

        """
        return self.board[coords[0]][coords[1]]

    def ascii_board(self):
        """
        Display an ascii map of the board, used for debugging purposes.

        """
        for x in range(0, 3):
            print("\n----------")
            for y in range(0, 3):
                print("|" + self.board[x][y] + "|", end="")

        print("\n----------")

    def register_update(self, what, *args):
        """
        Register a function for the game module to call when it
        updates the board.

        """
        print("register_update: %s" % what)
        d = {}
        d['function'] = what
        d['args'] = args
        print("register_update: %s" % repr(d))
        self.updates.append(d)

    def send_update(self):
        """
        Notify update functions that the board has been updated.

        """
        self.ascii_board()
        print(self.updates)
        for e in self.updates:
            e['function'](*e['args'])

    # Calling gtk.main from here breaks encapsulation,
    # so let's wrap it with these functions.
    def register_main_loop(self, what, *args):
        """
        Register main loop for game module to call.  Used for
        encapsulating away details (external loops) that don't matter here.

        """
        self.main_loop = {}
        self.main_loop['function'] = what
        self.main_loop['args'] = args

    def enter_main_loop(self):
        """
        Call the main loop specified.

        Note: THERE CAN BE ONLY ONE.

        """
        self.main_loop['function'](*self.main_loop['args'])

    def traverse_board(self, min=3, banned=[]):
        """
        Traverse the board and return the eight different pathways
        as a list of lists.

        min: the minimum number of continuous squares in a row.
                1, 2, and 3 are valid values.  (5 is right out)
        banned: list of symbols to ignore
        """

        min = 3 if min > 3 else 0 if min < 0 else min
        paths = []
        # rows
        for row in range(0, 3):
            pathway = []
            for col in range(0, 3):
                if self.square_lookup((row, col)) in banned:
                    continue
                else:
                    pathway.append((row, col))
            if len(pathway) >= min:
                paths.append(pathway)

        # columns
        for col in range(0, 3):
            pathway = []
            for row in range(0, 3):
                if self.square_lookup((row, col)) in banned:
                    continue
                else:
                    pathway.append((row, col))
            if len(pathway) >= min:
                paths.append(pathway)

        # diagonals
        pathway = []
        for row in range(0, 3):
            col = row  # diagonal magic
            if self.square_lookup((row, col)) in banned:
                continue
            else:
                pathway.append((row, col))
        if len(pathway) >= min:
            paths.append(pathway)

        pathway = []
        # Need to reverse the diagonal.  Subtracting
        # 2 and taking the absolute value yields the
        # appropriate numbers.
        for row in (range(0, 3)):
            col = abs(row-2)
            if self.square_lookup((row, col)) in banned:
                continue
            else:
                pathway.append((row, col))
        if len(pathway) >= min:
            paths.append(pathway)

        return paths

if __name__ == "__main__":
    import gui
    game = Game()
    ui = gui.GUI(game)
    game.gui = ui
    # This needs to be at the end.  Perhaps a priority system
    # is in order here.
    game.register_update(game.check_for_win)
    game.send_update()
    game.enter_main_loop()
