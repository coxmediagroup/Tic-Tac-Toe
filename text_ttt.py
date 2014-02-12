#!/usr/bin/env python

import sys
from ttt.game.game import AbstractGame
from ttt.player.player import AbstractPlayer, ComputerPlayer


class TextGame(AbstractGame):
    def display_board(self):

        pretty_board = []
        for i in xrange(self.board.size):
            if not self.board.squares[i]:
                pretty_board.append(i)
            else:
                pretty_board.append(self.board.squares[i])

        pb = pretty_board

        print ""
        print "   |   |   "
        print " %s | %s | %s " % (pb[0], pb[1], pb[2])
        print "   |   |   "
        print "---+---+---"
        print "   |   |   "
        print " %s | %s | %s " % (pb[3], pb[4], pb[5])
        print "   |   |   "
        print "---+---+---"
        print "   |   |   "
        print " %s | %s | %s " % (pb[6], pb[7], pb[8])
        print "   |   |   "
        print ""

    def display_finale(self):

        print ""
        print ""

        if not self.winner:
            print "You have fought to a draw"
        else:
            print "The winner is: %s" % self.winner

        print ""
        print ""


class TextPlayer(AbstractPlayer):
    def get_square(self, current_board, message):
        if message:
            print "** %s" % message

        try:
            rtn = raw_input("%s move> " % self.marker)
        except KeyboardInterrupt:
            rtn = None

        return rtn


def x_or_o():
    valid = ["X", "O"]
    answer = None
    while True:
        try:
            answer = raw_input("Are you X or O?> ").upper()
        except KeyboardInterrupt:
            return None

        if answer in valid:
            break
        print "Incorrect choice."

    return answer


def main():
    response = x_or_o()
    if not response:
        print ""
        return 1

    player1 = None
    player2 = None
    if response == "X":
        player1 = TextPlayer("X")
        player2 = ComputerPlayer("O")
    else:
        player1 = ComputerPlayer("X")
        player2 = TextPlayer("O")

    game = TextGame(player1, player2)
    game.play()
    print ""
    return 0

if __name__ == "__main__":
    sys.exit(main())
