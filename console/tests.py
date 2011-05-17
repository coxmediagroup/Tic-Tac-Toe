import unittest
import pdb
import random 
from tic_tac_toe import Board, BoardError, Player, ComputerPlayer

class BoardTest(unittest.TestCase):
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

class PersonTest(unittest.TestCase):

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

class ComputerPlayerTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.player = Player("X", self.board, "Allan")
        self.computer = ComputerPlayer("O",self.board )

    def test_place_marker(self):
        self.player.place_marker(4)
        self.computer.place_marker()
        assert self.board.last_cell != 4

class GameTest(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player = Player("X", self.board, "Sys")
        self.computer = ComputerPlayer("O",self.board)
    def test_one_game(self):
        sys_moves = []
        while self.board.winner == None:
            choice_made = False
            while not choice_made:
                choice = random.randrange(0, 9, 1)
                if choice not in sys_moves and self.board.get_cell(choice) == None:
                    sys_moves.append(choice)
                    choice_made = True
                    self.player.place_marker(choice)
                    if self.board.winner == None:
                        self.computer.place_marker()
        print "\n{0} is the winner with moves of {1} on board {2}\n".format(self.board.winner, sys_moves, self.board.grid )
if __name__ == "__main__":
    unittest.main()
