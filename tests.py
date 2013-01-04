import unittest
import tictactoe as ttt


class AIPlayerTests(unittest.TestCase):
    """Test the AIPlayer class"""

    def setUp(self):
        self.player = ttt.AIPlayer('X')
        self.player2 = ttt.Player('Y')

    def test_look_for_win_no_wins(self):
        """Test AIPlayer.look_for_win() when there are no possible wins"""

        board = ttt.Board()

        # Check several non-winning board layouts which
        # cover several distinct categories of situations
        self.assertEqual(None, self.player.look_for_win(board))

        board.tttboard = ['Y', None, 'Y',
                          None, None, None,
                          None, None, None]
        self.assertEqual(None, self.player.look_for_win(board))

        board.tttboard = ['X', None, None,
                          None, None, None,
                          None, None, None]
        self.assertEqual(None, self.player.look_for_win(board))

        board.tttboard = ['X', None, None,
                          None, None, 'X',
                          None, None, None]
        self.assertEqual(None, self.player.look_for_win(board))

    def test_look_for_win_winner(self):
        """Test AIPlayer.look_for_win() when there are possible wins"""

        board = ttt.Board()
        board.tttboard = ['X', None, 'X',
                          None, None, None,
                          None, None, None]
        self.assertEqual(1, self.player.look_for_win(board))

        board.tttboard = ['X', None, None,
                          None, None, None,
                          None, None, 'X']
        self.assertEqual(4, self.player.look_for_win(board))

    def test_pick_open_position(self):
        """Test AIPlayer.pick_open_position()"""

        board = ttt.Board()

        self.player.strategy = ttt.AIPlayer.STRATEGIES[3]
        self.assertEqual(4, self.player.pick_open_position(board))

        board.tttboard = [None, None, None,
                          None, 'X', None,
                          None, None, None]
        self.assertEqual(0, self.player.pick_open_position(board))

        board.tttboard = [None, None, None,
                          None, 'Y', None,
                          None, None, None]
        self.assertEqual(0, self.player.pick_open_position(board))

        board.tttboard = ['X', None, 'Y',
                          None, 'X', None,
                          'Y', 'X', 'Y']
        self.assertEqual(1, self.player.pick_open_position(board))

        board.tttboard = ['X', 'X', 'X',
                          'X', 'X', 'X',
                          'X', 'X', 'X']
        self.assertRaises(IndexError, self.player.pick_open_position, board)

    def test_take_turn_first_move(self):
        """Test AIPlayer.take_turn()"""

        board = ttt.Board()
        self.assertEqual(0, self.player.turn_count)

        position = self.player.take_turn(board, self.player2)
        self.assertEqual(1, self.player.turn_count)
        self.assertEqual(position, 4)

    # This method is way too long...
    # Break this up into per strategy tests?
    def test_take_turn_second_move(self):
        """Test AIPlayer.take_turn() on the second move"""

        board = ttt.Board()
        # Loop through each potential first move of player2 and make sure
        # that the correct strategy gets set and

        self.player.turn_count = 1
        board.tttboard = ['Y', None, None,
                          None, 'X', None,
                          None, None, None]
        position = self.player.take_turn(board, self.player2)
        self.assertEqual(2, self.player.turn_count)
        self.assertEqual(8, position)
        self.assertEqual(ttt.AIPlayer.STRATEGIES[0], self.player.strategy)

        self.player.turn_count = 1
        board.tttboard = [None, 'Y', None,
                          None, 'X', None,
                          None, None, None]
        position = self.player.take_turn(board, self.player2)
        self.assertEqual(2, self.player.turn_count)
        self.assertEqual(8, position)
        self.assertEqual(ttt.AIPlayer.STRATEGIES[1], self.player.strategy)

        self.player.turn_count = 1
        board.tttboard = [None, None, 'Y',
                          None, 'X', None,
                          None, None, None]
        position = self.player.take_turn(board, self.player2)
        self.assertEqual(2, self.player.turn_count)
        self.assertEqual(6, position)
        self.assertEqual(ttt.AIPlayer.STRATEGIES[2], self.player.strategy)

        self.player.turn_count = 1
        board.tttboard = [None, None, None,
                          'Y', 'X', None,
                          None, None, None]
        position = self.player.take_turn(board, self.player2)
        self.assertEqual(2, self.player.turn_count)
        self.assertEqual(0, position)
        self.assertEqual(ttt.AIPlayer.STRATEGIES[3], self.player.strategy)

        self.player.turn_count = 1
        board.tttboard = [None, None, None,
                          None, 'X', 'Y',
                          None, None, None]
        position = self.player.take_turn(board, self.player2)
        self.assertEqual(2, self.player.turn_count)
        self.assertEqual(0, position)
        self.assertEqual(ttt.AIPlayer.STRATEGIES[5], self.player.strategy)

        self.player.turn_count = 1
        board.tttboard = [None, None, None,
                          None, 'X', None,
                          'Y', None, None]
        position = self.player.take_turn(board, self.player2)
        self.assertEqual(2, self.player.turn_count)
        self.assertEqual(2, position)
        self.assertEqual(ttt.AIPlayer.STRATEGIES[6], self.player.strategy)

        self.player.turn_count = 1
        board.tttboard = [None, None, None,
                          None, 'X', None,
                          None, 'Y', None]
        position = self.player.take_turn(board, self.player2)
        self.assertEqual(2, self.player.turn_count)
        self.assertEqual(0, position)
        self.assertEqual(ttt.AIPlayer.STRATEGIES[7], self.player.strategy)

        self.player.turn_count = 1
        board.tttboard = [None, None, None,
                          None, 'X', None,
                          None, None, 'Y']
        position = self.player.take_turn(board, self.player2)
        self.assertEqual(2, self.player.turn_count)
        self.assertEqual(0, position)
        self.assertEqual(ttt.AIPlayer.STRATEGIES[8], self.player.strategy)


class BoardTests(unittest.TestCase):

    def setUp(self):
        self.player = ttt.Player('X')

    def test_select_position(self):
        """Tests Board.select_position()"""

        board = ttt.Board()
        board.select_position(0, self.player)
        self.assertEqual(board.tttboard[0], self.player.board_value)
        self.assertRaises(ttt.PositionAlreadyTakenError, board.select_position, 0, self.player)

    def test_check_for_win(self):
        """Tests Board.check_for_win()"""
        board = ttt.Board()

        self.assertFalse(board.check_for_win(self.player))

        for group in board.wins:
            board.tttboard = [None, None, None,
                              None, None, None,
                              None, None, None]

            for position in group:
                board.tttboard[position] = self.player.board_value

            self.assertTrue(board.check_for_win(self.player))

if __name__ == '__main__':
    unittest.main()

