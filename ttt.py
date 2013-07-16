#!/usr/bin/env python
from board import Board


def main():
    game_board = Board()
    while True:
        print "Classic Console Tic-Tac-Toe"
        print ""
        print "Make a selection:"
        print ""
        print "n) new game"
        print "q) quit"
        print "Enter your selection: "
        selection = raw_input()
        if selection in ("q", "Q"):
            break
        elif selection in ("p", "P"):
            game_board.print_board()


if __name__ == "__main__":
    main()
