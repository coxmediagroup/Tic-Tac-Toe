#!/usr/bin/env python
import tictactoe
import random


class StopGame(Exception):
    pass


def play_random_game():
    board = tictactoe.Board()
    human = tictactoe.PLAYER_X
    computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)
    move_list = []


    def check_winner():
        winner = board.get_winner()

        if winner is not None:
            if winner != computer.player:
                print "Move_List = "
                print move_list
                board.print_board()
                raise Exception("Computer Lost")

            raise StopGame()

        if len(board.get_available_moves()) == 0:
            raise StopGame()




    try:
        while True:
            move = random.choice(board.get_available_moves())
            move_list.append(move)
            board.add_move(move, human)
            check_winner()

            move = computer.get_next_move(board)
            move_list.append(move)
            board.add_move(move, computer.player)
            check_winner()
    except StopGame:
        pass


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print 'Must specify a run count'
        sys.exit(1)

    runcount = int(sys.argv[1])

    for run in range(runcount):
        play_random_game()

