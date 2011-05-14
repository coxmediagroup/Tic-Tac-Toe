#! /usr/bin/env python


class Board(object):

    BOARD_SIZE = 9

    def __init__(self):
        self.__board = []
        for i in range(Board.BOARD_SIZE):
            self.__board.append(None)

    def size(self):
        return len(self.__board)

    def take_cell(self, index, claim):
        self.__board[index] = claim

    def get_cell(self, index):
        return self.__board[index]




class Player(object):
    pass


class ComputerPlayer(Player):
    pass


class Game(object):
    pass
