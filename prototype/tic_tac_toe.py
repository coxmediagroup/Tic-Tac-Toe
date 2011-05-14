#! /usr/bin/env python


class BoardError(Exception): pass
class Board(object):

    BOARD_SIZE = 9

    def __init__(self):
        self.clear()

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

    def clear(self):
        self.__board = []
        for i in range(Board.BOARD_SIZE):
            self.__board.append(None)

    def __check_cells(self, index1, index2, index3):
        a,b,c = self.get_cell(index1), self.get_cell(index2), self.get_cell(index3)
        if a == None and b == None and c == None:
            return False
        return a == b and a == c

    def __check_rows(self):
        result = False
        result = self.__check_cells(0,1,2)
        if result == False:
            result = self.__check_cells(3,4,5)
        if result == False:
            result = self.__check_cells(6,7,8)
        return result

    def __check_columns(self):
        result = False
        result = self.__check_cells(0,3,6)
        if result == False:
            result = self.__check_cells(1,4,7)
        if result == False:
            result = self.__check_cells(2,5,8)
        return result

    def __check_diagonals(self):
        result = False
        result = self.__check_cells(0,4,8)
        if result == False:
            result = self.__check_cells(2,4,6)
        return result

    def check_board(self):
        result = False
        result = self.__check_rows()
        if result == False:
            result = self.__check_columns()
        if result == False:
            result = self.__check_diagonals()
        return result

class Player(object):
    pass


class ComputerPlayer(Player):
    pass


class Game(object):
    pass
