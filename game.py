#!/usr/bin/env python2

"""
Game logic code module.
"""

from __future__ import print_function

class Game:
    # List of functions to call when we update the board.
    updates = []
    main_loop = None

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
        mark = self.get_mark(player)
        print(mark, player)
        if self.board[x][y] == " ":
            self.board[x][y] = mark
            self.next_turn()
            return True
        return False

    def get_mark(self, player):
        return "X" if player == "human" else "O"

    def get_board(self):
        return self.board

    def next_turn(self):
        old = self.turn
        self.turn = "ai" if self.turn != "ai" else "human"
        print("Was %s's turn, now %s's." % (old, self.turn))
        self.check_ai_move()

    def check_ai_move(self):
        if self.turn == "ai":
            import ai
            valid_move = False
            while not valid_move:
                valid_move = ai.move(self)
            print("AI MOVED")
            self.send_update()

    def ascii_board(self):
        for x in range(0, 3):
            print("\n----------")
            for y in range(0, 3):
                print("|" + self.board[x][y] + "|", end="")

        print("\n----------")

    def register_update(self, what, *args):
        print("register_update: %s" % what)
        d = {}
        d['function'] = what
        d['args'] = args
        print("register_update: %s" % repr(d))
        self.updates.append(d)

    def send_update(self):
        self.ascii_board()
        print(self.updates)
        for e in self.updates:
            print("send_update: %s" % (e['args']))
            e['function'](*e['args'])

    # Calling gtk.main from here breaks encapsulation,
    # so let's wrap it with these functions.
    def register_main_loop(self, what, *args):
        self.main_loop = {}
        self.main_loop['function'] = what
        self.main_loop['args'] = args

    def enter_main_loop(self):
        self.main_loop['function'](*self.main_loop['args'])

if __name__ == "__main__":
    import gui
    game = Game()
    ui = gui.GUI(game)
    game.gui = ui
    game.send_update()
    game.enter_main_loop()
