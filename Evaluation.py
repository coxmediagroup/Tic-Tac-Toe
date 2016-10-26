#!/usr/bin/python

from Board import Board

class Evaluation:
    def __init__(self, board):
        self.board = board

    def __allSameAndValid(self, list):
        return all([l == list[0] and(list[0] == 'X' or list[0] == 'O') for l in list])

    def winner(self):
        layout = self.board.fetch()
        for i in [0, 1, 2]:
            if self.__allSameAndValid(layout[i]):
                return layout[i][0]
            if self.__allSameAndValid([row[i] for row in layout]):
                return layout[0][i]
        if self.__allSameAndValid([layout[0][0], layout[1][1], layout[2][2]]):
            return layout[1][1]
        if self.__allSameAndValid([layout[0][2], layout[1][1], layout[2][0]]):
            return layout[1][1]
        return None

    def isTie(self):
        if self.board.isFull() and self.winner() == None:
            return True
        return False
            
