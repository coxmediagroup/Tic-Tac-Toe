import unittest
import board

class BoardTest(unittest.TestCase):

    def setUp(self):
        self.board = board.Board()

    def test_initial_empty(self):
        for row in self.board.board:
            for position in row:
                self.assertEqual(position, board.EMPTY_MARKER)

    def test_move_marks_board(self):
        self.board.move('X', 0, 0)
        self.assertEqual(self.board.board[0][0], 'X')
        self.board.move('O', 1, 0)
        self.assertEqual(self.board.board[0][1], 'O')

    def test_out_of_bounds_move_rejected(self):
        self.assertRaises(IndexError, self.board.move, 'X',-1,0)
        self.assertRaises(IndexError, self.board.move, 'X', 3,0)

    def test_occupied_move_rejected(self):
        self.board.move('X', 0, 0)
        self.assertRaises(ValueError, self.board.move, 'O', 0, 0)

    def test_empty_squares(self):
        expectedAvailable = [(x,y) for x in range(3) for y in range(3)]
        self.assertEqual(self.board.getEmptySquares(), expectedAvailable)
        while len(expectedAvailable) > 0:
            position = expectedAvailable.pop()
            self.board.move('X', position[0], position[1])
            self.assertEqual(self.board.getEmptySquares(), expectedAvailable)

    def test_finished(self):
        self.assertEqual(self.board.finished(),(False, None))
        #horizontal win
        self.board.move('X', 0, 0)
        self.board.move('X', 1, 0)
        self.board.move('X', 2, 0)
        self.assertEqual(self.board.finished(), (True, 'X'))
        self.board.reset()
        #vertical win
        self.board.move('O', 0, 0)
        self.board.move('O', 0, 1)
        self.board.move('O', 0, 2)
        self.assertEqual(self.board.finished(), (True, 'O'))
        self.board.reset()
        #diagonal wins
        self.board.move('X', 0, 0)
        self.board.move('X', 1, 1)
        self.board.move('X', 2, 2)
        self.assertEqual(self.board.finished(), (True, 'X'))
        self.board.reset()
        self.board.move('O', 2, 0)
        self.board.move('O', 1, 1)
        self.board.move('O', 0, 2)
        self.assertEqual(self.board.finished(), (True, 'O'))
        #tie
        self.board.reset()
        self.board.move('O', 0, 0)
        self.board.move('X', 0, 1)
        self.board.move('X', 1, 0)
        self.board.move('O', 1, 1)
        self.board.move('O', 0, 2)
        self.board.move('O', 1, 2)
        self.board.move('X', 2, 2)
        self.board.move('O', 2, 1)
        self.board.move('X', 2, 0)
        self.assertEqual(self.board.finished(), (True, None))



if __name__ == "__main__":
    unittest.main()
