#! /usr/bin/env python


class BoardError(Exception): pass
class Board(object):

    BOARD_SIZE = 9

    def __init__(self):
        self.__board = []
        for i in range(Board.BOARD_SIZE):
            self.__board.append(None)

    def size(self):
        return len(self.__board)

    def take_cell(self, index, claim):
        if index < self.BOARD_SIZE:
            if self.__board[index] == None:
                self.__board[index] = claim
            else:
                raise BoardError, "{0} already taken".format(index)
        else:
            raise BoardError, "{0} off board".format(index)


    def get_cell(self, index):
        if index < self.BOARD_SIZE:
            return self.__board[index]
        else:
            raise BoardError, "{0} off board".format(index)




class Player(object):
    pass


class ComputerPlayer(Player):
    pass


class Game(object):
    pass
