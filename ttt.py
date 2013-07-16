#!/usr/bin/env python
"""
Main program to run Tic-Tac-Toe on the console.
"""
from board import Board
from errors import TicTacToeError
import random


def is_user_first():
    """
    Roll two simulated dice until one is greater than the other. Whoever has the highest roll is first.

    @return: True if the user is first, otherwise False (if the computer is first).
    @rtype: bool
    """
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


def take_turn(game_board, position, user_mark):
    """
    Take a single turn by adding C{user_mark} to C{position} on the given C{game_board}. If the board remains
    playable after that, the computer will automatically take a turn using its AI to find the next move.

    @param game_board: The game board to take the turn on
    @type game_board: L{board.Board}
    @param position: The absolute position to mark
    @type position: int
    @param user_mark: The letter to mark on the board
    @type user_mark: str
    """
    try:
        game_board.add_mark(position, user_mark)
    except TicTacToeError as err:
        print err
        return
    if game_board.is_playable:
        other_mark = "O" if user_mark in ('x', "X") else "X"
        game_board.add_mark(game_board.find_next_move(other_mark), other_mark)


def main():
    """
    Run the main program!
    """
    game_board = Board()
    while True:
        print "Classic Console Tic-Tac-Toe"
        print ""
        print "Make a selection:"
        print ""
        print "n) new game"
        print "p) print the board"
        print "q) quit"
        print "0-8) make the given move"
        print ""
        print "Enter your selection: "
        selection = raw_input()
        if selection in ("q", "Q"):
            break
        elif selection in ("p", "P"):
            game_board.print_board()
        elif selection in ("n", "N"):
            game_board = Board()
            if not is_user_first():
                game_board.add_mark(game_board.find_next_move("X"), "X")
        elif selection in ('0', '1', '2', '3', '4', '5', '6', '7', '8'):
            position = int(selection)
            take_turn(game_board, position, "O")


if __name__ == "__main__":  # pragma: no cover
    main()
