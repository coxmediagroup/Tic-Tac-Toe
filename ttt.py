#!/usr/bin/env python
from board import Board
import random
from errors import TicTacToeError


def is_user_first():
    while True:
        user_dice = random.randrange(1, 7)
        comp_dice = random.randrange(1, 7)
        print "Rolling dice to see who goes first..."
        print ""
        print "You rolled {0}".format(user_dice)
        print "Computer rolled {0}".format(comp_dice)
        if user_dice > comp_dice:
            print "User is first"
            return True
        elif user_dice < comp_dice:
            print "Computer is first"
            return False
        else:
            print "Dice are tied, rolling again..."


def main():
    game_board = Board()
    while True:
        print "Classic Console Tic-Tac-Toe"
        print ""
        print "Make a selection:"
        print ""
        print "n) new game"
        print "p) print the board"
        print "q) quit"
        print "1-9) make the given move"
        print ""
        print "Enter your selection: "
        selection = raw_input()
        if selection in ("q", "Q"):
            break
        elif selection in ("p", "P"):
            game_board.print_board()
        elif selection in ("n", "N"):
            game_board = Board()


if __name__ == "__main__":
    main()
