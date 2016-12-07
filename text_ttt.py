#!/usr/bin/env python

import sys
import argparse
import ttt


class TextGame(ttt.AbstractGame):
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
            print "The winner is: %s" % self.winner.marker

        print ""
        print ""


class TextPlayer(ttt.AbstractPlayer):
    def get_square(self, current_board, previous_move, message):
        if message:
            print "** %s" % message

        try:
            rtn = raw_input("%s move> " % self.marker)
        except KeyboardInterrupt:
            rtn = None

        return rtn


def get_human_count():
    valid = [0, 1, 2]
    answer = None
    while True:
        try:
            answer = raw_input("# of human players? [0,1,2]> ")
            answer = int(answer)
        except KeyboardInterrupt:
            return None
        except ValueError:
            pass

        if answer in valid:
            break

        print "Invalid number."

    return answer


def get_x_or_o():
    valid = ["X", "O"]
    answer = None
    while True:
        try:
            answer = raw_input("Which marker are you? [X,O]> ").upper()
        except KeyboardInterrupt:
            return None

        if answer in valid:
            break
        print "Incorrect choice."

    return answer


def get_cmd_args():
    parser = argparse.ArgumentParser(description="Text Based Tic-Tac-Toe")
    parser.add_argument(
        "-p",
        dest="humans",
        type=int,
        help="# of human players. [0|1|2]")
    parser.add_argument(
        "-m",
        dest="marker",
        help="marker to use in single human player game [X|O]")
    args = parser.parse_args()

    return args.humans, args.marker.upper() if args.marker else None


def main():
    humans, marker = get_cmd_args()

    if humans is None:
        humans = get_human_count()

    if humans is None:
        print ""
        return 0

    if humans not in [0, 1, 2]:
        print ""
        print "Invalid number of human players"
        return 1

    if humans == 1 and marker is None:
        marker = get_x_or_o()

    if humans == 1 and marker is None:
        print ""
        return 0

    if humans == 1 and marker not in ["X", "O"]:
        print ""
        print "Invalid marker option"
        return 1

    player1 = None
    player2 = None

    if humans == 0:
        player1 = ttt.ComputerPlayer("X")
        player2 = ttt.ComputerPlayer("O")
    elif humans == 1:
        if marker == "X":
            player1 = TextPlayer("X")
            player2 = ttt.ComputerPlayer("O")
        else:
            player1 = ttt.ComputerPlayer("X")
            player2 = TextPlayer("O")
    else:
        player1 = TextPlayer("X")
        player2 = TextPlayer("O")

    game = TextGame(player1, player2)
    game.play()
    print ""
    return 0

if __name__ == "__main__":
    sys.exit(main())
