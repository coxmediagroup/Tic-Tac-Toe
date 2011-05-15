"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


from models import Board, BoardError, Player, ComputerPlayer

class BoardTest(TestCase):
    def setUp(self):
        self.board = Board()

    def test_size(self):
        self.assertEquals(self.board.size(), 9)

    def test_take_cell(self):
        marker = "X"
        self.assertEquals(self.board.get_cell(0), None)
        self.board.take_cell(0, marker)
        self.assertEquals(self.board.get_cell(0), marker)
        self.assertRaises(BoardError,self.board.take_cell, 9, marker)
        self.assertRaises(BoardError, self.board.take_cell, 0, "O")

    def test_check_board_incomplete(self):
        marker = "O"
        self.board.clear()
        self.board.take_cell(0,marker)
        # pdb.set_trace()
        assert self.board.check_board() == False
        assert self.board.winner != marker

    def test_check_board_horizontal(self):
        marker = "O"
        self.board.take_cell(0,marker)
        self.board.take_cell(1,marker)
        self.board.take_cell(2,marker)
        assert self.board.check_board()
        assert self.board.winner == marker
        self.board.clear()
        self.board.take_cell(3,marker)
        self.board.take_cell(4,marker)
        self.board.take_cell(5,marker)
        assert self.board.check_board()
        assert self.board.winner == marker
        self.board.clear()
        self.board.take_cell(6,marker)
        self.board.take_cell(7,marker)
        self.board.take_cell(8,marker)
        assert self.board.check_board()
        assert self.board.winner == marker

    def test_check_board_vertical(self):
        marker = "O"
        self.board.take_cell(0,marker)
        self.board.take_cell(3,marker)
        self.board.take_cell(6,marker)
        assert self.board.check_board()
        assert self.board.winner == marker
        self.board.clear()
        self.board.take_cell(1,marker)
        self.board.take_cell(4,marker)
        self.board.take_cell(7,marker)
        assert self.board.check_board()
        assert self.board.winner == marker
        self.board.clear()
        self.board.take_cell(2,marker)
        self.board.take_cell(5,marker)
        self.board.take_cell(8,marker)
        assert self.board.check_board()
        assert self.board.winner == marker

    def test_check_board_diagonal(self):
        marker = "O"
        self.board.take_cell(0,marker)
        self.board.take_cell(4,marker)
        self.board.take_cell(8,marker)
        assert self.board.check_board()
        assert self.board.winner == marker
        self.board.clear()
        self.board.take_cell(2,marker)
        self.board.take_cell(4,marker)
        self.board.take_cell(6,marker)
        assert self.board.check_board()
        assert self.board.winner == marker

class PersonTest(TestCase):

    def setUp(self):
        self.player = Player()

    def test_marker(self):
        assert self.player.marker == None
        self.player.marker = "X"
        assert self.player.marker == "X"

    def test_board(self):
        assert self.player.board == None
        self.player.board = Board()
        assert self.player.board != None

    def test_name(self):
        assert self.player.name == None
        self.player.name = "Allan"
        assert self.player.name == "Allan"
    def test_place_marker(self):
        board = Board()
        self.player = Player("X",board, "Allan")
        self.player.place_marker(4)
        assert board.get_cell(4) == "X"

class ComputerPlayerTest(TestCase):

    def setUp(self):
        self.board = Board()
        self.player = Player("X", self.board, "Allan")
        self.computer = ComputerPlayer("O",self.board )

    def test_place_marker(self):
        self.player.place_marker(4)
        self.computer.place_marker()
        assert self.board.last_cell != 4
