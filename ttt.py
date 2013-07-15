#!/usr/bin/env python


def print_board():
    print "   |   |   "
    print " X | O |   "
    print "   |   |   "
    print "---|---|---"
    print "   |   |   "
    print " O | X | O "
    print "   |   |   "
    print "---|---|---"
    print "   |   |   "
    print " X |   | O "
    print "   |   |   "


def main():
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
            print_board()


if __name__ == "__main__":
    main()
