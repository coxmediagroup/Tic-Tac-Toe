"""
Tests checking against the Space and Board classes

"""
import unittest
from board import Board, BoardSpace, MIN_DIM, MAX_DIM

class TestSpace(unittest.TestCase):
    """
    Testing the space class
    
    """
    def setUp(self):
        self.board_space = BoardSpace(player=u"X", board_index=1)
    
    def test_new_space(self):
        self.assertEqual(str(self.board_space), "X")

class TestBoard(unittest.TestCase):
    """
    Testing the Board class
    
    """
    def setUp(self):
        self.board = Board()
    
    def test_new_board(self):
        """
        Game boards should have a string representation of the current
        game state.
        
        """
        # If this is a new board then all the spaces should be blank
        # i.e. character for player0 * row count * column count
        string_representation = (self.board.player0 *
                                 self.board.rows *
                                 self.board.cols)
        self.assertEqual(str(self.board), string_representation)
        
        # the board is really just a two-dimensional list, so first check
        # that there are the expected amount of "rows"
        self.assertEqual(len(self.board.board), self.board.rows)
        
        # then check the expected amount of "columns" for each row
        all_columns = all(len(x) == self.board.cols for x in self.board.board)
        self.assertTrue(all_columns)
    
    def test_board_positions(self):
        """
        smallest board:
         
         1 | 2 | 3
        --- --- ---
         4 | 5 | 6
        --- --- ---
         7 | 8 | 9
        
        biggest board:
         
         1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13| 14| 15| 16
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
         17| 18| 19| 20| 21| 22| 23| 24| 25| 26| 27| 28| 29| 30| 31| 32
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
         33| 34| 35| 36| 37| 38| 39| 40| 41| 42| 43| 44| 45| 46| 47| 48
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
         49| 50| 51| 52| 53| 54| 55| 56| 57| 58| 59| 60| 61| 62| 63| 64
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
         65| 66| 67| 68| 69| 70| 71| 72| 73| 74| 75| 76| 77| 78| 79| 80
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
         81| 82| 83| 84| 85| 86| 87| 88| 89| 90| 91| 92| 93| 94| 95| 96
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
         97| 98| 99|100|101|102|103|104|105|106|107|108|109|110|111|112
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        113|114|115|116|117|118|119|120|121|122|123|124|125|126|127|128
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        129|130|131|132|133|134|135|136|137|138|139|140|141|142|143|144
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        145|146|147|148|149|150|151|152|153|154|155|156|157|158|159|160
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        161|162|163|164|165|166|167|168|169|170|171|172|173|174|175|176
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        177|178|179|180|181|182|183|184|185|186|187|188|189|190|191|192
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        193|194|195|196|197|198|199|200|201|202|203|204|205|206|207|208
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        209|210|211|212|213|214|215|216|217|218|219|220|221|222|223|224
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        225|226|227|228|229|230|231|232|233|234|235|236|237|238|239|240
        --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        241|242|243|244|245|246|247|248|249|250|251|252|253|254|255|256
        
        """
        for row_count in range(MIN_DIM, MAX_DIM+1):
            for col_count in range(MIN_DIM, MAX_DIM+1):
                board = Board(rows=row_count, cols=col_count)
                last_space_on_board = board.board[-1][-1].board_index
                
                for x_pos in range(1, last_space_on_board+1):
                    row, col = board.board_position_by_index(x_pos)
                    board_space_index = board.board[row][col].board_index
                    msg = "board.board[{}][{}].board_index == {} (It is {}!)"
                    msg = msg.format(row, col, x_pos, board_space_index)
                    board_index = board.board[row][col].board_index
                    self.assertEqual(board_index, x_pos, msg)

class TestBoardMoves(unittest.TestCase):
    """
    Test board game moves
    
    """
    def test_win_by_row(self):
        """row win check"""
        board = Board()
        board.board[0][0].player = board.player1
        board.board[0][1].player = board.player1
        board.board[0][2].player = board.player1
        self.assertTrue(board.player_win_round(board.player1))
    
    def test_win_by_column(self):
        """column win check"""
        board = Board()
        board.board[0][0].player = board.player1
        board.board[1][0].player = board.player1
        board.board[2][0].player = board.player1
        self.assertTrue(board.player_win_round(board.player1))
    
    def test_win_by_diagonal_left_to_right(self):
        """diagonal win check (rotated)"""
        board = Board()
        board.board[0][0].player = board.player1
        board.board[1][1].player = board.player1
        board.board[2][2].player = board.player1
        self.assertTrue(board.player_win_round(board.player1))
        
    def test_win_by_diagonal_right_to_left(self):
        """diagonal win check (counter-rotated)"""
        board = Board()
        board.board[0][2].player = board.player1
        board.board[1][1].player = board.player1
        board.board[2][0].player = board.player1
        self.assertTrue(board.player_win_round(board.player1))
        
    def test_remainging_spaces(self):
        """
        As the board spaces get occupied the board should accurately report
        the remaining spaces
        
        """
        # The default board has 9 spaces therefore a new board should report
        # 9 remaining spaces
        board = Board()
        self.assertEqual(len(board.remaining_spaces()), 9)
        
        # After each space is occupied the remaining spaces should be
        # accurately decremented
        board.board[0][0].player = board.player1
        self.assertEqual(len(board.remaining_spaces()), 8)
        
        board.board[0][1].player = board.player2
        self.assertEqual(len(board.remaining_spaces()), 7)
        
        board.board[0][2].player = board.player1
        self.assertEqual(len(board.remaining_spaces()), 6)
        
        board.board[1][0].player = board.player2
        self.assertEqual(len(board.remaining_spaces()), 5)
        
        board.board[1][1].player = board.player1
        self.assertEqual(len(board.remaining_spaces()), 4)
        
        board.board[1][2].player = board.player2
        self.assertEqual(len(board.remaining_spaces()), 3)
        
        board.board[2][0].player = board.player1
        self.assertEqual(len(board.remaining_spaces()), 2)
        
        board.board[2][1].player = board.player2
        self.assertEqual(len(board.remaining_spaces()), 1)
        
        board.board[2][2].player = board.player1
        self.assertEqual(len(board.remaining_spaces()), 0)
        
class TestScoreBoard(unittest.TestCase):
    """
    Testing basic score keeping
    
    """
    def setUp(self):
        self.board = Board()
    
    def _player_score(self, this_player, point=1):
        """Simple DRY"""
        # new board does not have a score
        self.assertEqual(self.board.score_board[this_player], 0)
        # increment the score
        self.board.score_board[this_player] += 1
        self.assertEqual(self.board.score_board[this_player], 1)
    
    def test_player_0_score(self):
        """player 0 represents the tied-game count"""
        self._player_score(self.board.player0)
    
    def test_player_1_score(self):
        """player 1 represents the initial player"""
        self._player_score(self.board.player1)
        
    def test_player_2_score(self):
        """player 2 represents the player whose turn is after player 1"""
        self._player_score(self.board.player2)
        
class TestGameBoardAI(unittest.TestCase):
    """
    Testing basic ai moves
    
    """
    def setUp(self):
        # AI should place player on board
        self.board = Board()
    
    def test_ai_place_a_move(self):
        # default empty board has 9 spaces
        self.assertEqual(len(self.board.remaining_spaces()), 9)
        # After first move there should be 8 spaces left
        self.board.ai_move()
        self.assertEqual(len(self.board.remaining_spaces()), 8)
    
    def _check_board_state(self, expected_board_state):
        """Keeping the check DRY"""
        # And check that the board state is how we expect it to be
        current_board_state = str(self.board)
        move_msg = 'Expected board state from player "{}" is "{}", not "{}"'
        msg = move_msg.format(self.board.player1, expected_board_state,
                              current_board_state)
        self.assertEqual(current_board_state, expected_board_state, msg)
    
    def test_ai_place_winning_move(self):
        """
        Given the current board has an obvious winning win for player 1 ("X")
        
            O O -
            X X -
            O - X
        
        Then the AI should place a winning move for player 1:
        
            O O -
            X X X
            O - X
        
        """
        # set up for new board
        self.board.clear_board()
        self.board.board[0][0].player = self.board.player2 #1
        self.board.board[0][1].player = self.board.player2 #2
        self.board.board[1][0].player = self.board.player1 #4
        self.board.board[1][1].player = self.board.player1 #5
        self.board.board[2][0].player = self.board.player2 #7
        self.board.board[2][2].player = self.board.player1 #9
        self.board.this_player = self.board.player1
        self.board.next_player = self.board.player2
        
        # AI places a move for player 1
        self.board.ai_move()
        
        # And check that the board state is how we expect it to be
        self._check_board_state('OO-XXXO-X')
    
    def test_ai_place_blocking_move(self):
        """
        Given that player 1 has a potential winning move for the next round:

            X X -
            - - O
            O - -
        
        Then the AI should place a blocking move for player 2:
        
            X X O
            - - O
            O - -
        
        """
        # set up for new board
        self.board.clear_board()
        self.board.board[0][0].player = self.board.player1 #1
        self.board.board[0][1].player = self.board.player1 #2
        self.board.board[1][2].player = self.board.player2 #6
        self.board.board[2][0].player = self.board.player2 #7
        self.board.this_player = self.board.player2
        self.board.next_player = self.board.player1
        
        # AI places a move for player 2
        self.board.ai_move()
        
        # And check that the board state is how we expect it to be
        self._check_board_state('XXO--OO--')
    
    def test_ai_places_remaining_moves_unwinnable(self):
        """
        Given the board state is not winnable
        
        X O X
        - X -
        O X O
        
        Let the AI play the next two rounds and confirm is not winnable
        
        (player 2)

            X O X
            O X -
            O X O
        
        (player 1)

            X O X
            O X X
            O X O
        
        """
        self.board.clear_board()

        self.board.board[0][0].player = self.board.player1 #1
        self.board.board[0][1].player = self.board.player2 #2
        self.board.board[0][2].player = self.board.player1 #3
        self.board.board[1][1].player = self.board.player1 #5
        self.board.board[2][0].player = self.board.player2 #7
        self.board.board[2][1].player = self.board.player1 #8
        self.board.board[2][2].player = self.board.player2 #9
        
        self.board.this_player = self.board.player2
        self.board.next_player = self.board.player1
        self.board.ai_move()
        self.board.ai_move()
        
        # assert board.player_win_round(board.player2) == True
        msg = 'Board should be not be winnable: "{}"'
        self.assertFalse(self.board.winning_space(), msg.format(self.board))

    def test_ai_place_obvious_win(self):
        """
        Testing ai_move for preference of obvious winning move
        
        With minmax and AB pruning the obvious winning move is occasionally
        in a pruned branch leaving the AI to be seemingly a little bit less
        intelligent than we would like.
        
        Given this board state:
        
            X X O
            - - -
            - - O
        
        With the minimax and AB pruning algorithm, the AI would place the
        the next move at:
        
            X X O
            O - -
            - - O
        
        But the obvious winning move should be postion #4
        
            X X O
            - - O
            - - O

        """
        # AI should place winning move
        self.board.clear_board()
    
        self.board.board[0][0].player = self.board.player1 #1
        self.board.board[0][1].player = self.board.player1 #2
        self.board.board[0][2].player = self.board.player2 #3
        self.board.board[2][2].player = self.board.player2 #9
        
        # set up for new board
        self.board.this_player = self.board.player2
        self.board.next_player = self.board.player1
        self.board.ai_move()
    
        self._check_board_state('XXO--O--O')

if __name__ == '__main__':
    unittest.main()
