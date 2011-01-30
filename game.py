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

    def __init__(self):
        self.initialize()

    def initialize(self):
        """
        Need this in a seperate function so New can restart.

        """
        # Disable turns so resetting the board isn't counted
        # as human moves.
        self.turn = None
        self.board = {}
        for x in range(0, 3):
            self.board[x] = {}
            for y in range(0, 3):
                self.board[x][y] = " "
        self.send_update()
        import random
        self.turn = random.choice(["human", "ai"])
        print("%s's turn." % self.turn)
        self.check_ai_move()

    def move(self, player, x, y, test=False):
        """
        Add a move to the game board.
        returns True if move is valid, False otherwise.

        player: "human" or "ai"
        test: if test=True, copy the board, make the move
              and return the board for viewing.

        """
        mark = self.get_mark(player)
        from copy import copy
        board = self.board if not test else copy(board)
        # If spot is blank, add, otherwise don't.
        if board[x][y] == " ":
            board[x][y] = mark
            if test:
                return board
            self.send_update()
            self.next_turn()
            return True
        return False

    def get_opponent(self, player):
        """
        Return the opponent's 'name'

        """
        return "ai" if player == "human" else "human"

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
            while not valid_move and self.turn:
                valid_move = ai.move("ai", self)
        self.send_update()

    def check_for_win(self):
        """
        See if there is a winner.

        """
        winner = None

        paths = self.traverse_board()

        x_wins = self.traverse_board(requires={"X": 3})
        y_wins = self.traverse_board(requires={"O": 3})
        winner = x_wins if x_wins else y_wins if y_wins else None
        if winner:
            self.turn = None
            # traverse_board returns paths, and we know each symbol
            # is identical, so grab the first one in the nested list.
            print("Victory: %s" % winner)
            print("Winner: %s" % self.square_lookup(winner[0][0]))

    def check_for_draw(self):
        """
        See if the game is a draw.

        """
        
        open_spaces = self.traverse_board(requires={" ": 1})
        if not open_spaces:
            self.turn = None
            print("Oh, all right, we'll call it a draw.")

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
        d = {}
        d['function'] = what
        d['args'] = args
        self.updates.append(d)

    def send_update(self):
        """
        Notify update functions that the board has been updated.

        """
        #self.ascii_board()
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

    def check_requirements(self, pathway, requires):
        """
        Check a pathway against the stated requirements.
        
        """
        contents = {}
        for e in pathway:
            val = self.square_lookup(e)
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

    def traverse_board(self, banned=[], requires={}):
        """
        Traverse the board and return the eight different pathways
        as a list of lists.

        banned: ignore pathways if they contain these symbols
        requires: {"X": 3}, etc.  {symbol, required number}
        """

        min = 3
        paths = []
        # rows
        for row in range(0, 3):
            pathway = []
            passes_reqs = True
            for col in range(0, 3):
                if self.square_lookup((row, col)) in banned:
                    continue
                else:
                    pathway.append((row, col))
            if(len(pathway) >= min
                    and self.check_requirements(pathway, requires)):
                paths.append(pathway)

        # columns
        for col in range(0, 3):
            pathway = []
            for row in range(0, 3):
                if self.square_lookup((row, col)) in banned:
                    continue
                else:
                    pathway.append((row, col))
            if(len(pathway) >= min
                    and self.check_requirements(pathway, requires)):
                paths.append(pathway)

        # diagonals
        pathway = []
        for row in range(0, 3):
            col = row  # diagonal magic
            if self.square_lookup((row, col)) in banned:
                continue
            else:
                pathway.append((row, col))
        if(len(pathway) >= min
                and self.check_requirements(pathway, requires)):
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
        if(len(pathway) >= min
                and self.check_requirements(pathway, requires)):
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
    # Must be after win.  Priority system?
    # Probably too much trouble for just these two.   
    game.register_update(game.check_for_draw)
    game.send_update()
    game.enter_main_loop()
