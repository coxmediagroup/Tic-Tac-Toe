#!/usr/bin/python

from Board import Board
from Evaluation import Evaluation
from AI import AI
from View import View

class Game:
    def __init__(self):
        self.board = Board()
        self.evaluation = Evaluation(self.board)
        self.view = View(self.board)

    def __finish(self, computerPlayer):
        if self.evaluation.winner() == computerPlayer:
            print "Computer player wins"
        elif self.evaluation.isTie():
            print "Tie game"
        else:
            print "Human player wins"

    def run(self):
        startPlayer = self.view.inputStartPlayer()
        computerPlayer = 'X' if startPlayer == 2 else 'O'
        ai = AI(computerPlayer, self.board)
        while self.evaluation.winner() == None and not self.evaluation.isTie():
            self.view.displayBoard()
            if self.board.getPlayer() == computerPlayer:
                ai.makeMove()
            else:
                move = self.view.inputMove()
                self.board.move(move)
        self.view.displayBoard()
        self.__finish(computerPlayer)
        
    
